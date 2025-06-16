from weather import get_weather

clima = get_weather()


if "erro" not in clima:
    print(clima)