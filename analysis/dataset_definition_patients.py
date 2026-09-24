# from ehrql import create_dataset
# from ehrql.tables.tpp import patients, practice_registrations

# dataset = create_dataset()

# index_date = "2020-03-31"

# has_registration = practice_registrations.for_patient_on(
#     index_date
# ).exists_for_patient()

# dataset.define_population(has_registration)

# dataset.sex = patients.sex
# dataset.age = patients.age_on(index_date)

from ehrql import create_dataset
from ehrql.tables.core import patients, clinical_events

dataset = create_dataset()
dataset.configure_dummy_data(population_size=50)

age = patients.age_on("2020-03-31")
first_event_date = clinical_events.sort_by(clinical_events.date).first_for_patient().date

dataset.define_population((age > 18) & (age < 80))
dataset.age = age
dataset.sex = patients.sex
dataset.first_event_date = first_event_date
dataset.after_dob = first_event_date > patients.date_of_birth
dataset.before_dod = (first_event_date < patients.date_of_death) | patients.date_of_death.is_null()

