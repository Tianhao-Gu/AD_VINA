# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except ImportError:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class CompoundSetUtils(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login',
            service_ver='release',
            async_job_check_time_ms=100, async_job_check_time_scale_percent=150, 
            async_job_check_max_time_ms=300000):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = service_ver
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc,
            async_job_check_time_ms=async_job_check_time_ms,
            async_job_check_time_scale_percent=async_job_check_time_scale_percent,
            async_job_check_max_time_ms=async_job_check_max_time_ms)

    def compound_set_from_file(self, params, context=None):
        """
        CompoundSetFromFile
        string staging_file_path
        :param params: instance of type "compoundset_upload_params" ->
           structure: parameter "workspace_id" of String, parameter
           "staging_file_path" of String, parameter "compound_set_name" of
           String, parameter "mol2_staging_file_path" of String
        :returns: instance of type "compoundset_upload_results" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "compoundset_ref" of type "obj_ref"
        """
        return self._client.run_job('CompoundSetUtils.compound_set_from_file',
                                    [params], self._service_ver, context)

    def compound_set_to_file(self, params, context=None):
        """
        CompoundSetToFile
        string compound_set_name
        string output_format
        :param params: instance of type "compoundset_download_params" ->
           structure: parameter "compound_set_ref" of String, parameter
           "output_format" of String
        :returns: instance of type "compoundset_download_results" ->
           structure: parameter "file_path" of String, parameter
           "packed_mol2_files_path" of String, parameter
           "comp_id_mol2_file_name_map" of mapping from String to String
        """
        return self._client.run_job('CompoundSetUtils.compound_set_to_file',
                                    [params], self._service_ver, context)

    def compound_set_from_model(self, params, context=None):
        """
        CompoundSetFromModel
        required:
        string workspace_id
        string model_ref
        string compound_set_name
        :param params: instance of type "compoundset_from_model_params" ->
           structure: parameter "workspace_id" of String, parameter
           "model_ref" of String, parameter "compound_set_name" of String
        :returns: instance of type "compoundset_upload_results" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "compoundset_ref" of type "obj_ref"
        """
        return self._client.run_job('CompoundSetUtils.compound_set_from_model',
                                    [params], self._service_ver, context)

    def export_compoundset_as_tsv(self, params, context=None):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        return self._client.run_job('CompoundSetUtils.export_compoundset_as_tsv',
                                    [params], self._service_ver, context)

    def export_compoundset_as_sdf(self, params, context=None):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        return self._client.run_job('CompoundSetUtils.export_compoundset_as_sdf',
                                    [params], self._service_ver, context)

    def export_compoundset_mol2_files(self, params, context=None):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "export_mol2_files_results" -> structure:
           parameter "packed_mol2_files_path" of String, parameter
           "comp_id_mol2_file_name_map" of mapping from String to String
        """
        return self._client.run_job('CompoundSetUtils.export_compoundset_mol2_files',
                                    [params], self._service_ver, context)

    def convert_compoundset_mol2_files_to_pdbqt(self, params, context=None):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "convert_mol2_files_results" -> structure:
           parameter "packed_pdbqt_files_path" of String, parameter
           "comp_id_pdbqt_file_name_map" of mapping from String to String
        """
        return self._client.run_job('CompoundSetUtils.convert_compoundset_mol2_files_to_pdbqt',
                                    [params], self._service_ver, context)

    def fetch_mol2_files_from_zinc(self, params, context=None):
        """
        :param params: instance of type "FetchZINCMol2Params" -> structure:
           parameter "workspace_id" of String, parameter "compoundset_ref" of
           type "obj_ref", parameter "over_write" of Long
        :returns: instance of type "compoundset_upload_results" -> structure:
           parameter "report_name" of String, parameter "report_ref" of
           String, parameter "compoundset_ref" of type "obj_ref"
        """
        return self._client.run_job('CompoundSetUtils.fetch_mol2_files_from_zinc',
                                    [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.run_job('CompoundSetUtils.status',
                                    [], self._service_ver, context)
