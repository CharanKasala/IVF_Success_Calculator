from django.shortcuts import render

# Create your views here.

import os
import math
import pandas as pd
import numpy as np

def index(request):

    if request.method == 'POST':
        age=int(request.POST['age'])
        weight=int(request.POST['weight'])
        height_feet=int(request.POST['height_feet'])
        height_inches=int(request.POST['height_inches'])
        
        attempted_ivf_previously=request.POST['previous_ivf']
        if(attempted_ivf_previously == 'TRUE'):
            param_attempted_ivf_previously=True
        elif(attempted_ivf_previously =='FALSE'):
            param_attempted_ivf_previously=False
        elif(attempted_ivf_previously == "N/A"):
            param_attempted_ivf_previously=np.nan

        #print("attempted ivf prev",attempted_ivf_previously)

        no_of_prev_preg=request.POST.get('no_of_prev_preg')
        no_of_live_births=request.POST.get('no_of_live_births')

        
        male_factor_infertility=request.POST.get('male_factor_infertility')=='TRUE'
        endometriosis=request.POST.get('endometriosis')=='TRUE'
        tubal_factor=request.POST.get('tubal_factor')=='TRUE'
        ovulatory_disorder=request.POST.get('ovulatory_disorder')=='TRUE'
        diminished_ovarian_reserve=request.POST.get('diminished_ovarian_reserve')=='TRUE'
        uterine_factor=request.POST.get('uterine_factor')=='TRUE'
        other_reason=request.POST.get('other_reason')=='TRUE'
        unexplained_fertility=request.POST.get('unexplained_fertility')=='TRUE'
        
        param_is_reason_for_infertility_known=request.POST.get('reason_not_known') != 'TRUE'
        

        param_using_own_eggs=request.POST.get('own_eggs') == 'TRUE'

        """
        print("param_using_own_eggs",param_using_own_eggs)
        print("param_attempted_ivf_previously",param_attempted_ivf_previously)
        print("param_is_reason_for_infertility_known",param_is_reason_for_infertility_known)

        print("age",age)
        print("weight",weight)
        print("height_feet",height_feet,"height_inches",height_inches)
        print("no_of_prev_preg",no_of_prev_preg)
        print("no_of_live_births",no_of_live_births)

        print("male_factor_infertility",male_factor_infertility)
        print("endometriosis",endometriosis)
        print("tubal_factor",tubal_factor)
        print("ovulatory disorder",ovulatory_disorder)
        print("diminished_ovarian_reserve",diminished_ovarian_reserve)
        print("uterine_factor",uterine_factor)
        print("other_reason",other_reason)
        print("unexplained_fertility",unexplained_fertility)
    
        """
    
        curr_dir=os.path.dirname(__file__)
        file_path=os.path.join(curr_dir,'data','ivf_success_formulas.csv')
        #print(file_path)

        pd.set_option('display.float_format', '{:.8f}'.format)
        data_frame=pd.read_csv(file_path)

        user_bmi =((weight)/((height_feet*12+height_inches)**2))*703

        filtered_data=data_frame[
            (data_frame['param_using_own_eggs'] == param_using_own_eggs) &
            ((data_frame['param_attempted_ivf_previously'] == param_attempted_ivf_previously) | pd.isna(data_frame['param_attempted_ivf_previously'])) &
            (data_frame['param_is_reason_for_infertility_known'] == param_is_reason_for_infertility_known) 
        ]

        #print(filtered_data)

        if(filtered_data.empty):
            print("No matching data found for given input")
            return render(request, 'calculator/index.html', {'error_message': 'No matching data found for given input'})

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
    
        
        return render(request, 'calculator/index.html',{'success_rate': success_rate*100})
    
    return render(request, 'calculator/index.html')