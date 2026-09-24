from ehrql import create_dataset, months
from ehrql.tables.core import patients, ons_deaths
from ehrql.tables.tpp import apcs, practice_registrations

# The following dataset definition that identifies patients who have an ONS death record with an underlying cause of death recorded, and who were hospitalised 6 months before their death.

# It also extracts information about where the patients live, and their underlying cause of death (an ICD-10 code). A downstream analysis script will use this data to analyse regional variations in the cause of death, and identify the prevalence of ICD-10 codes for heart failure (I50, I500, I501, I509) by region.

study_start_date = "2022-01-01"
study_end_date = "2023-01-01"

died_in_study_period = ons_deaths.date.is_on_or_between(
    study_start_date, study_end_date
)

hospitalisation_in_6_months_before_death = (
    apcs
    .where(
        apcs.admission_date.is_on_or_between(
            (ons_deaths.date - months(6)), ons_deaths.date
        )
    )
    .sort_by(apcs.admission_date)
    .last_for_patient()
)
hospitalised_date = hospitalisation_in_6_months_before_death.admission_date

# registration info at ons-registered date of death
registration = practice_registrations.for_patient_on(ons_deaths.date)

dataset = create_dataset()

dataset.region = registration.practice_nuts1_region_name

dataset.cause_of_death = ons_deaths.underlying_cause_of_death
dataset.date_of_death = ons_deaths.date

dataset.hospitalised_date = hospitalised_date

dataset.define_population(
    died_in_study_period
    & hospitalised_date.is_not_null()
    & ons_deaths.underlying_cause_of_death.is_not_null()
)