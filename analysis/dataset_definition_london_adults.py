from ehrql import create_dataset
from ehrql.tables.core import patients
from ehrql.tables.tpp import addresses


min_age = 18
max_age = 80

age = patients.age_on("2024-01-01")

dataset = create_dataset()
dataset.age = age

london_msoa = (
    addresses
    .where(addresses.msoa_code == "E02000001")
    .sort_by(addresses.start_date)
    .last_for_patient()
)

dataset.define_population(
    (age >= min_age)
    & (age <= max_age)
    & london_msoa.exists_for_patient()
)
dataset.msoa = london_msoa.msoa_code