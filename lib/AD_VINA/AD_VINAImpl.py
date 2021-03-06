# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os, sys, shutil
import uuid

from installed_clients.WorkspaceClient import Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.ProteinStructureUtilsClient import ProteinStructureUtils
from installed_clients.CompoundSetUtilsClient import CompoundSetUtils
from installed_clients.DataFileUtilClient import DataFileUtil

from .util.KBaseObjUtil import *
from .util.PrintUtil import *
from .util.HTMLUtil import *


#END_HEADER


class AD_VINA:
    '''
    Module Name:
    AD_VINA

    Module Description:
    A KBase module: AD_VINA
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/Tianhao-Gu/AD_VINA.git"
    GIT_COMMIT_HASH = "0908067c13fef943fd9df6349e7361259f017317"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        cls = self.__class__

        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.workspace_url = config['workspace-url']
        cls.shared_folder = config['scratch']
        cls.testData_dir = '/kb/module/test/data'
        cls.config = config

        cls.suffix = '_' + str(uuid.uuid4())

        ws = Workspace(self.workspace_url)
        dfu = DataFileUtil(self.callback_url)
        psu = ProteinStructureUtils(self.callback_url)
        csu = CompoundSetUtils(self.callback_url)


        attr_d = {
            'ws': ws,
            'dfu': dfu,
            'psu': psu,
            'csu': csu,
            'callback_url': cls.callback_url,
            'workspace_url': cls.workspace_url,
            'shared_folder': cls.shared_folder,
            'testData_dir': cls.testData_dir,
            'suffix': cls.suffix
            }

        VarStash.update(attr_d)

        dprint("sys.path", "os.environ", run=globals())
        dprint('config', run=locals())

        
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                            level=logging.INFO)

        #END_CONSTRUCTOR
        pass


    def ad_vina(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN ad_vina


        VarStash.update({
            'ctx': ctx,
            'workspace_id': params['workspace_id']
            })

        ctx_censored = ctx.copy()
        ctx_censored.pop('token')
        

        dprint('params', 'ctx_censored', run=locals())


        ##
        ####
        ###### param validation
        ###### and defaulting
        ####
        ##


        params_search_space = params['search_space']


        ##
        ## if center specified, must be completely specified

        key_center_l = ['center_' + ch for ch in list('xyz')]
        center_xyz = [params_search_space[key] for key in key_center_l]

        if any(center_xyz) and not all(center_xyz):
            raise ValueError(
                'INPUT ERROR: '
                'If any of center (i.e., center_x, center_y, center_z) is specified, all of center must be specified. '
                'Please try again'
                )


        """
        ##
        ## must specify center to specify any of size

        key_size_l = ['size_' + ch for ch in list('xyz')]
        size_xyz = [params_search_space[key] for key in key_size_l]

        if not all(center_xyz) and any(size_xyz):
            raise ValueError(   
                "INPUT ERROR: "
                "Must completely specify center (i.e., center_x, center_y, center_z) before specifying any of size (i.e., size_x, size_y, size_z). "
                "(Also, if any of size is unspecified, it will default to 30 Angstroms.) "
                "Please try again"
                )
        """


        ##
        ## if center specified, fill in default size

        size_default = 30 # Angstroms

        key_size_l = ['size_' + ch for ch in list('xyz')]
        size_xyz = [params_search_space[key] for key in key_size_l]

        if all(center_xyz) and not all(size_xyz):
            for key_size in key_size_l:
                if not params_search_space.get(key_size):
                    params_search_space[key_size] = size_default



        ##
        ####
        ###### dl
        ####
        ##


        ps = ProteinStructure(params['pdb_ref'])
        ps.calc_center_size()
        ps.convert_to_pdbqt()

        cs = CompoundSet(params['ligand_list_ref'])
        cs.split_multiple_models()

        dprint(ChemKBaseObj.created_instances)



        ##
        ####
        ###### params
        ###### run
        ####
        ##


        ##

        params_static = {
            'cpu': 4
            }

        params_default = {
            'num_modes': 1000,
            'energy_range': 10,
            'exhaustiveness': 20,
            }

        ##

        key_search_space_l = key_center_l + key_size_l
        key_misc_l = ['num_modes', 'energy_range', 'seed', 'exhaustiveness']

        ##

        out_pdbqt_filename_l = []
        log_filename_l = []


        ##
        ## for each ligand

        for ligand_name, ligand_pdbqt_filepath in zip(cs.pdbqt_compound_l, cs.pdbqt_filepath_l):

            if params.get('skip_vina'):
                break

            run_name = ligand_name + '_vs_' + ps.name

            out_pdbqt_filename_l.append(run_name + '.pdbqt')
            log_filename_l.append(run_name + '.log')

            ##
            ## set up default params

            params_vina = {
                'receptor': ps.pdbqt_filepath,
                'ligand': ligand_pdbqt_filepath,
                'log': run_name + '.log',
                'out': run_name + '.pdbqt',
                **params_static,
                **params_default
            }

            for space_coords_name in ['center', 'size']:
                space_coords = getattr(ps, space_coords_name)
                for k, v in zip(list('xyz'), space_coords):
                    params_vina[space_coords_name + '_' + k] = v

            ##
            ## check for search_space and misc params

            for key in key_misc_l:
                if params.get(key):
                    params_vina[key] = params[key]

            for key in key_search_space_l:
                if params_search_space.get(key):
                    params_vina[key] = params_search_space[key]


            ##
            ##

            cmd = 'vina'

            for param, arg in params_vina.items():
                cmd += ' --' + param + ' ' + str(arg)

            """
            _cmd = ( f"vina --receptor {ps.pdbqt_filepath} --ligand {ligand_pdbqt_filepath} "
                     f"--cpu 4 --log {run_name + '.log'} "
                     f"--center_x {ps.center[0]} --center_y {ps.center[1]} --center_z {ps.center[2]} "
                     f"--size_x {ps.size[0]} --size_y {ps.size[1]} --size_z {ps.size[2]} "
                     f"--out {run_name + '.pdbqt'}" )
            """

            retcode, stdout, stderr = dprint(cmd, run='cli', subproc_run_kwargs={'cwd': VarStash.shared_folder})
            if retcode != 0:
                sep = '--------------------------------------------------------------------------'
                raise RuntimeError(
                        f"AutoDock terminated abnormally with error message: "
                        f"[{stderr}] "
                        "You can check logs (click 'Job Status' tab in upper right of cell) for more information"
                        )

            if params.get('skip_most_vina'):
                break



        ##
        ####
        ###### html
        ####
        ##

        hb = HTMLBuilder(ps, cs)



        ##
        ####
        ###### return directories
        ####
        ##


        def dir_to_shock(dir_path, name, description):
            '''
            For regular directories or html directories
            
            name - for regular directories: the name of the flat file returned to ui
                   for html directories: the name of the html file
            '''
            dfu_fileToShock_ret = VarStash.dfu.file_to_shock({
                'file_path': dir_path,
                'make_handle': 0,
                'pack': 'zip',
                })

            dir_shockInfo = {
                'shock_id': dfu_fileToShock_ret['shock_id'],
                'name': name,
                'description': description
                }

            return dir_shockInfo

        # return files

        dir_retFiles_path = os.path.join(self.shared_folder, 'pdbqt_log_dir')
        os.mkdir(dir_retFiles_path)


        for filename in out_pdbqt_filename_l + log_filename_l:
            shutil.copyfile(os.path.join(self.shared_folder, filename), os.path.join(dir_retFiles_path, filename))

        # so DataFileUtil doesn't crash over zipping an empty folder
        if len(os.listdir(dir_retFiles_path)) == 0:
            dprint(rf"echo 'Sorry, no files were generated' > {os.path.join(dir_retFiles_path, 'README')}", run='cli')

        dir_retFiles_shockInfo = dir_to_shock(dir_retFiles_path, 'pdbqt_log.zip', 'Generated .pdbqt and log files')



        # html

        html_shockInfo = dir_to_shock(hb.html_dir, 'index.html', 'HTML report for AutoDock Vina')
            


        ##
        ####
        ###### report
        ####
        ##

        report_params = {
            'message': 'this is the report_params `message`',
            'warnings': ['this is the', 'report_params `warnings`'],
            'direct_html_link_index': 0, #?0
            'html_links': [html_shockInfo],
            'file_links': [dir_retFiles_shockInfo],
            'report_object_name': 'autodock_vina' + self.suffix,
            'workspace_name': params['workspace_name'],
            }

        kbr = KBaseReport(self.callback_url)
        report_output = kbr.create_extended_report(report_params)

        output = {
            'report_name': report_output['name'],
            'report_ref': report_output['ref'],
        }



        #END ad_vina

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method ad_vina return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def mol2_to_pdbqt(self, ctx, mol2_file_path, compound_id):
        """
        :param mol2_file_path: instance of String
        :param compound_id: instance of String
        :returns: instance of String
        """
        # ctx is the context object
        # return variables are: pdbqt_file_path
        #BEGIN mol2_to_pdbqt

        cs = CompoundSet('', get_file='do_nothing')

        pdbqt_file_path = cs.mol2_to_pdbqt(mol2_file_path, self.shared_folder, compound_id)
        #END mol2_to_pdbqt

        # At some point might do deeper type checking...
        if not isinstance(pdbqt_file_path, str):
            raise ValueError('Method mol2_to_pdbqt return value ' +
                             'pdbqt_file_path is not type str as required.')
        # return the results
        return [pdbqt_file_path]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
