'''
Created on Mar 26, 2018

@author: ckubudi
'''
import itertools
import tqdm
import hashlib
import os
import zipfile
import shutil
import copy
from multiprocessing import Pool

class Multi_Run(object):

    def __init__(self, algorithm,hedge_file=None,processes=None):
        '''
        Constructor
        '''
        self.algorithm=algorithm
        self.result_filename=algorithm.name+'.txt'
        self.hedged_result_filename=hedge_file
        self.processes=processes
        if self.hedged_result_filename:
            self.result_hedged_filename=algorithm.name+'_hedged.txt'
        
    def get_params_combination(self, factor_params_list):
        temp=[factor_params_list[k] for k in factor_params_list]
        temp=list(itertools.product(*temp))
        factor_params_names=[k for k in factor_params_list]
        factor_params=[]
        for params in temp:
            my_params={}
            for i in range(len(factor_params_names)):
                my_params[factor_params_names[i]]=params[i]
            factor_params.append(my_params)
        
        return factor_params
    
    def delete_all_files(self,folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def save_result(self, f, result, param_values, plot_dir, is_header):
        if(is_header):
            f.write(self.algorithm.get_parameters_names()+","+result.get_output_stats_names()+"\n")
        f.write(self.algorithm.get_parameters_values()+","+result.get_output_stats_results()+"\n")
        
        m=hashlib.md5()
        temp='['+param_values+']'
        m.update(temp.encode(encoding='UTF-8').upper())
        filename=m.hexdigest().upper()
        result.r_cum.to_csv(os.path.join(plot_dir,filename)+'.txt', date_format='%Y%m%d', header=False)

    def create_plot_dir(self, output_file_path, filename):
        plot_dirname=os.path.join(output_file_path,filename+"_ProfitData")
        if not os.path.exists(plot_dirname):
            os.makedirs(plot_dirname)
        return plot_dirname
    
    
    def zipdir(self, path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), arcname=file)
    
    def run_multiple(self, algorithm_params_list, returns,start_date='1990-01-01',end_date='2020-01-01',output_file_path='.//results//'):
        algorithm_params_dict_list=self.get_params_combination(algorithm_params_list)
        is_header=True

        #create result folder
        if not os.path.exists(output_file_path):
            os.makedirs(output_file_path)

        f=open(os.path.join(output_file_path,self.result_filename) , "w")
        plot_dir=self.create_plot_dir(output_file_path, self.result_filename)
        
        if self.hedged_result_filename:
            f_hedged=open(os.path.join(output_file_path,self.result_hedged_filename), "w")
            plot_hedged_dir=self.create_plot_dir(output_file_path, self.result_hedged_filename)
        
        """    
                for algorithm_params in tqdm.tqdm_notebook(algorithm_params_dict_list):
                    running_algo = copy.copy(self.algorithm)
                    running_algo.set_params(algorithm_params)
                    result=running_algo.run(returns,start_date,end_date,show_progress_bar=False)
                    self.save_result(f, result, running_algo.get_parameters_values(), plot_dir, is_header)
                    if self.hedged_result_filename:
                        hedged_result=result.get_hedged_result(self.hedged_result_filename)
                        self.save_result(f_hedged,hedged_result, running_algo.get_parameters_values(), plot_hedged_dir, is_header)
                    is_header=False    
        """
        ###########################                
        total = len(algorithm_params_dict_list)
        print("Starting multi-threading for {} params".format(total))
        with Pool(self.processes) as pool:
            all_results = list(tqdm.tqdm_notebook(pool.imap(Runner(self, returns, start_date, end_date), algorithm_params_dict_list),total=total))

        for r in all_results:
            params, result, hedged_result = r
            self.save_result(f, result, params, plot_dir, is_header)
            if self.hedged_result_filename:
                self.save_result(f_hedged,hedged_result, params, plot_hedged_dir, is_header)
            is_header=False
        ###########################            
        f.close()
        
        zipf = zipfile.ZipFile(os.path.join(output_file_path,self.result_filename+'_ProfitData')+'.zip', 'w', zipfile.ZIP_DEFLATED)
        self.zipdir(plot_dir, zipf)
        shutil.rmtree(plot_dir)
        
        if self.hedged_result_filename:
            zipf = zipfile.ZipFile(os.path.join(output_file_path,self.result_hedged_filename+'_ProfitData')+'.zip', 'w', zipfile.ZIP_DEFLATED)
            self.zipdir(plot_hedged_dir, zipf)
            f_hedged.close()
            shutil.rmtree(plot_hedged_dir)
             #self.zipdir(plot_hedged_dir, zipf)
        
class Runner(object):
    def __init__(self, multi_run, returns, start_date, end_date):
        self.returns = returns
        self.start_date = start_date
        self.end_date = end_date
        self.multi_run = multi_run

    def __call__(self, params):
        return self.multi_run.run_unique(self.returns, self.start_date, self.end_date, params)        
