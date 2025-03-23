from aiohttp import web
import hashlib
from utils.database import get_connection

TOROX_SECRET_KEY = 'ec7127442c37359eabfa7194f13733cd'

async def torox_postback(request):
    params = request.rel_url.query

    oid = params.get('oid')
    user_id = params.get('user_id')
    amount = params.get('amount')
    sig = params.get('sig')
    conv_id = params.get('id')
    currency_name = params.get('currency_name')
    payout = params.get('payout')
    o_name = params.get('o_name')

    # Проверка подписи
    hash_str = f"{oid}-{user_id}-{TOROX_SECRET_KEY}"
    expected_sig = hashlib.md5(hash_str.encode()).hexdigest()

    if sig != expected_sig:
        print("❌ Неверная подпись постбэка от Torox")
        return web.Response(text='0')

    # Сохраняем транзакцию в БД
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, type, currency, status, created_at) VALUES (?, ?, ?, ?, ?, datetime('now'))",
        (user_id, amount, 'начисление', currency_name, 'success')
    )

    cursor.execute(
        "UPDATE balances SET amount = amount + ? WHERE user_id = ?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()

    print(f"✅ Конверсия от Torox: user {user_id}, сумма {amount}, оффер {o_name}")
    return web.Response(text='1')

async def start_postback_server():
    app = web.Application()
    app.router.add_get('/torox', torox_postback)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    print("🚀 Postback-сервер запущен на порту 8080")
