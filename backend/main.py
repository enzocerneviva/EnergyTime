from weather import get_weather

cidade = "São Paulo"
clima = get_weather()


if "erro" not in clima:
    print(clima)