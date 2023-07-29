from django.shortcuts import render

from .exchnge_rate_getter import ExchangeRateGetter


exchange_rate_getter = ExchangeRateGetter(target_currency=('USD', 'EUR'))


def index(request):
    exchange_rate_getter.load_currency_data()

    context ={
        'today': f'({exchange_rate_getter.days.today})',
        'yesterday': f'({exchange_rate_getter.days.yesterday})',
        'day_before_yesterday': f'({exchange_rate_getter.days.day_before_yesterday})',
        **exchange_rate_getter.get_today_rate(),
    }
    return render(
        request,
        template_name='exchange_rates/index.html',
        context=context,
    )
