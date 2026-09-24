from ehrql import create_dataset
from ehrql.tables.core import patients
from ehrql.tables.tpp import addresses

dataset = create_dataset()
dataset.configure_dummy_data(population_size=50)
age = patients.age_on("2024-01-01")

possible_msoas = ["E02000001", "E02000002", "E02000003", "E02000004"]

address = (
    addresses
    .where(addresses.msoa_code.is_in(possible_msoas))
    .sort_by(addresses.end_date)
    .last_for_patient()
)

no_address = ~addresses.exists_for_patient()

dataset.age = age
dataset.msoa = address.msoa_code

dataset.define_population(
    patients.exists_for_patient()
    & (address.exists_for_patient() | no_address)
)