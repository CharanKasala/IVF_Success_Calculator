
import pandas as pd
import math

age=32
weight=150
height_feet=5
height_inches=8

tubal_factor= True
male_factor_infertility= False
endometriosis= False
ovulatory_disorder= False
diminished_ovarian_reserve=True
uterine_factor= False
other_reason= False
unexplained_fertility= False

no_of_prev_preg=1
no_of_live_births=1

user_bmi =((weight)/((height_feet*12+height_inches)**2))*703

print("BMI IS", user_bmi )

param_using_own_eggs=True
param_attempted_ivf_previously= True
param_is_reason_for_infertility_known= True

pd.set_option('display.float_format', '{:.8f}'.format)
data_frame=pd.read_csv('ivf_success_formulas.csv')


filtered_data=data_frame[
    (data_frame['param_using_own_eggs'] == param_using_own_eggs) &
    (data_frame['param_attempted_ivf_previously'] == param_attempted_ivf_previously) &
    (data_frame['param_is_reason_for_infertility_known'] == param_is_reason_for_infertility_known)
]

print(filtered_data)

formula_intercept=filtered_data['formula_intercept']

formula_age_linear_coefficient=filtered_data['formula_age_linear_coefficient'].values
formula_age_power_coefficient=filtered_data['formula_age_power_coefficient'].values
formula_age_power_factor=filtered_data['formula_age_power_factor'].values


formula_bmi_linear_coefficient=filtered_data['formula_bmi_linear_coefficient'].values
formula_bmi_power_coefficient=filtered_data['formula_bmi_power_coefficient'].values
formula_bmi_power_factor=filtered_data['formula_bmi_power_factor'].values

tubal_factor_str='formula_tubal_factor_'+str(tubal_factor).lower()+'_value'
formula_tubal_factor_value=filtered_data[tubal_factor_str].values

male_factor_infertility_str='formula_male_factor_infertility_'+str(male_factor_infertility).lower()+'_value'
formula_male_factor_infertility_value=filtered_data[male_factor_infertility_str].values

endometriosis_str='formula_endometriosis_'+str(endometriosis).lower()+'_value'
formula_endometriosis_value=filtered_data[endometriosis_str].values

ovulator_disorder_str='formula_ovulatory_disorder_'+str(ovulatory_disorder).lower()+'_value'
formula_ovulatory_disorder_value=filtered_data[ovulator_disorder_str].values

diminished_ovarian_reserve_str='formula_diminished_ovarian_reserve_'+str(diminished_ovarian_reserve).lower()+'_value'
formula_diminished_ovarian_reserve_value=filtered_data[diminished_ovarian_reserve_str].values

uterine_factor_str='formula_uterine_factor_'+str(uterine_factor).lower()+'_value'
formula_uterine_factor_value=filtered_data[uterine_factor_str].values

other_reason_str='formula_other_reason_'+str(other_reason).lower()+'_value'
formula_other_reason_value=filtered_data[other_reason_str].values

unexplained_fertility_str='formula_unexplained_infertility_'+str(unexplained_fertility).lower()+'_value'
formula_unexplained_infertility_value=filtered_data[unexplained_fertility_str].values

no_of_prev_preg_str='formula_prior_pregnancies_'+str(no_of_prev_preg)+'_value'
formula_prior_pregnancies_value =filtered_data[no_of_prev_preg_str].values

no_of_live_births_str='formula_prior_live_births_'+str(no_of_live_births)+'_value'
formula_live_births_value=filtered_data[no_of_live_births_str].values


score= formula_intercept +  (formula_age_linear_coefficient * age) + (formula_age_power_coefficient) * (age ** formula_age_power_factor) 
score= score + (formula_bmi_linear_coefficient * user_bmi) + (formula_bmi_power_coefficient) * (user_bmi ** formula_bmi_power_factor)
score= score + formula_tubal_factor_value + formula_male_factor_infertility_value + formula_endometriosis_value + formula_ovulatory_disorder_value + formula_diminished_ovarian_reserve_value + formula_uterine_factor_value + formula_other_reason_value + formula_unexplained_infertility_value + formula_prior_pregnancies_value + formula_live_births_value

e=math.e

success_rate= (float)((e ** score)/(1+e ** score))

print("success_rate is",success_rate*100)
    