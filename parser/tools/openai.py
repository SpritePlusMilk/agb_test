import logging
from os import getenv
from typing import TYPE_CHECKING

from asgiref.sync import sync_to_async
from django.db.models import Count, F, Q, Sum
from django.template.loader import render_to_string
from django.utils.timezone import now
from openai import OpenAI

from parser.consts import CATEGORY_CHOICES
from parser.models import SalesAnalysis, Xml
from parser.tools import retry

from .exceptions import AnalysisRefused

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletion, ChatCompletionMessage


logger = logging.getLogger('xml_data_logger')


class OpenAiClient:
    def __init__(self) -> None:
        self.client: OpenAI = OpenAI(
            api_key=getenv('OPENAI_API_KEY', 'Test'),
        )
        self.model: str = getenv('OPENAI_MODEL', 'gpt-4o')

    async def do_request(self, prompt: str) -> tuple[str, bool]:
        response: 'ChatCompletion' = await self.client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ],
            model=self.model,
        )
        message: 'ChatCompletionMessage' = response.choices[0].message
        return (message.content, True) if message.content else (message.refusal, False)


openai_client = OpenAiClient()


@sync_to_async
def get_llm_prompt(xml_file: Xml) -> str:
    products = xml_file.products.all()
    aggregation_options = {category[1]: Count('pk', filter=Q(category=category[0])) for category in CATEGORY_CHOICES}
    context = {
        'date': xml_file.date,
        'top_products': products.order_by('quantity')[:3].values('name', 'quantity'),
        'categories': products.aggregate(**aggregation_options),
        'total_revenue': products.annotate(revenue=F('quantity') * F('price')).aggregate(Sum('revenue'))[
            'revenue__sum'
        ],
    }
    prompt = render_to_string('parser/prompt_template.txt', context)
    logger.warning(f'{now()}: Сформирован запрос на анализ продаж от {xml_file.date}:\n {prompt}')

    return prompt


async def save_analysis_result(xml_file: Xml, prompt_text: str, response_text: str) -> None:
    logger.warning(f'{now()}: Получена аналитика продаж на основе xml-файла от {xml_file.date}:\n {response_text}')
    await SalesAnalysis.objects.acreate(xml_file=xml_file, prompt=prompt_text, text=response_text)


@retry(tries=3, delay=10, delay_step=10, max_delay=60)
async def request_llm_analysis(xml_file: Xml) -> None:
    prompt = await get_llm_prompt(xml_file)
    response, is_successful = openai_client.do_request(prompt)

    if not is_successful:
        logger.warning(f'{now()}: Не получилось запросить аналитику продаж на основе xml-файла от {xml_file.date}')
        raise AnalysisRefused('Аналитика не может быть получена на данный момент')

    await save_analysis_result(xml_file, prompt, response)
