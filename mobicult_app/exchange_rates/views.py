from django.shortcuts import render

from .exchnge_rate_getter import ExchangeRateGetter


exchange_rate_getter = ExchangeRateGetter(target_currency=('USD', 'EUR'))


def _get_rate_page(request, rates: dict[str, float], day: str):
    context = {
        'active_page': day,
        'today': f'({exchange_rate_getter.days.today})',
        'yesterday': f'({exchange_rate_getter.days.yesterday})',
        'day_before_yesterday': f'({exchange_rate_getter.days.day_before_yesterday})',
        **rates,
    }
    return render(
        request,
        template_name='exchange_rates/index.html',
        context=context,
    )


def index(request):
    exchange_rate_getter.load_currency_data()
    return _get_rate_page(
        request,
        rates=exchange_rate_getter.get_today_rate(),
        day=f'сегодня ({exchange_rate_getter.days.today})'
    )

def yesterday(request):
    rates = exchange_rate_getter.get_yesterday_rate()

    if not rates:
        exchange_rate_getter.load_currency_data()
        rates = exchange_rate_getter.get_yesterday_rate()

    return _get_rate_page(
        request,
        rates,
        day=f'вчера ({exchange_rate_getter.days.yesterday})',
    )


def day_before_yesterday(request):
    rates = exchange_rate_getter.get_day_before_yesterday_rate()

    if not rates:
        exchange_rate_getter.load_currency_data()
        rates = exchange_rate_getter.get_day_before_yesterday_rate()

    return _get_rate_page(
        request,
        rates,
        day=f'позавчера ({exchange_rate_getter.days.day_before_yesterday})'
    )
