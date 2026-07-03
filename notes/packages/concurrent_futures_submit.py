from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Dict
import time

executor = ThreadPoolExecutor()


def get_transaction() -> Dict[str, Any]:
    time.sleep(1)
    return {"amount": 1_000 * 100}  # 1_000 rub in kopecks


def get_usd_rate() -> int:
    time.sleep(2)
    return 5_898  # rate in kopecks


def convert_to_usd(future1: Future[Dict[str, Any]], future2: Future[int]) -> int:
    transaction = future1.result()
    usd_rate = future2.result()
    return transaction["amount"] / usd_rate


transaction_future = executor.submit(get_transaction)
usd_rate_future = executor.submit(get_usd_rate)

amount_in_usd = convert_to_usd(transaction_future, usd_rate_future)
print(f"We've got ${amount_in_usd}")
