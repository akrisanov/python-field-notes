import asyncio


async def count(number):
    return number if number > 50 else None


async def main():
    tasks = [asyncio.create_task(count(number)) for number in range(100)]

    for index, find_number in enumerate(tasks, start=1):
        if result := await find_number:
            print(f"Found at the {index} place:")
            break
    else:
        result = "Not found"

    print(result)

    # another option is to use asyncio.as_completed ------------------------------------------------

    tasks = [count(number) for number in range(100)]

    # automatically wraps the count function in a task
    for find_number in asyncio.as_completed(tasks):
        try:
            result = await find_number
        except (asyncio.CancelledError, Exception) as exc:
            breakpoint()
        print("Trying as_completed here:", result)


asyncio.run(main())
