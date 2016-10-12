# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
The reg module provides classes for interfacing with the `niftyreg
<http://niftyreg.sourceforge.net>`_ registration command line tools.
The interfaces were written to work with niftyreg version 1.4
"""

import os
import warnings

from nipype.interfaces.niftyreg.base import (get_custom_path, NiftyRegCommand)
from nipype.utils.filemanip import split_filename
from nipype.interfaces.base import (TraitedSpec, File, traits, isdefined, CommandLineInputSpec)

warn = warnings.warn
warnings.filterwarnings('always', category=UserWarning)


# A custom trait class for positive integers
class PositiveInt (traits.BaseInt):
    # Define the default value
    default_value = 0
    # Describe the trait type
    info_text = 'A positive integer'

    def validate(self, obj, name, value):
        value = super(PositiveInt, self).validate(obj, name, value)
        if (value >= 0) == 1:
            return value
        self.error(obj, name, value)


class RegAladinInputSpec(CommandLineInputSpec):
    # Input reference file
    ref_file = File(exists=True, desc='The input reference/target image',
                    argstr='-ref %s', mandatory=True)
    # Input floating file
    flo_file = File(exists=True, desc='The input floating/source image',
                    argstr='-flo %s', mandatory=True)
    # No symmetric flag
    nosym_flag = traits.Bool(argstr='-noSym', desc='Turn off symmetric registration')
    # Rigid only registration
    rig_only_flag = traits.Bool(argstr='-rigOnly', desc='Do only a rigid registration')
    # Directly optimise affine flag
    aff_direct_flag = traits.Bool(argstr='-affDirect', desc='Directly optimise the affine parameters')
    # Input affine
    in_aff_file = File(exists=True, desc='The input affine transformation',
                       argstr='-inaff %s')
    # Input reference mask
    rmask_file = File(exists=True, desc='The input reference mask',
                      argstr='-rmask %s')
    # Input floating mask
    fmask_file = File(exists=True, desc='The input floating mask',
                      argstr='-fmask %s')
    # Maximum number of iterations
    maxit_val = PositiveInt(desc='Maximum number of iterations', argstr='-maxit %d')
    # Multiresolution levels
    ln_val = PositiveInt(desc='Number of resolution levels to create', argstr='-ln %d')
    # Number of resolution levels to process
    lp_val = PositiveInt(desc='Number of resolution levels to perform', argstr='-lp %d')
    # Smoothing to apply on reference image
    smoo_r_val = traits.Float(desc='Amount of smoothing to apply to reference image',
                              argstr='-smooR %f')
    # Smoothing to apply on floating image
    smoo_f_val = traits.Float(desc='Amount of smoothing to apply to floating image',
                              argstr='-smooF %f')
    # Use nifti header to initialise transformation
    nac_flag = traits.Bool(desc='Use nifti header to initialise transformation',
                           argstr='-nac')
    # Use the input masks centre of mass to initialise the transformation
    cog_flag = traits.Bool(desc='Use the input masks centre of mass to initialise the transformation',
                           argstr='-cog')
    # Percent of blocks that are considered active.
    v_val = PositiveInt(desc='Percent of blocks that are active', argstr='-pv %d')
    # Percent of inlier blocks
    i_val = PositiveInt(desc='Percent of inlier blocks', argstr='-pi %d')
    # Lower threshold on reference image
    ref_low_val = traits.Float(desc='Lower threshold value on reference image',
                               argstr='-refLowThr %f')
    # Upper threshold on reference image
    ref_up_val = traits.Float(desc='Upper threshold value on reference image',
                              argstr='-refUpThr %f')
    # Lower threshold on floating image
    flo_low_val = traits.Float(desc='Lower threshold value on floating image',
                               argstr='-floLowThr %f')
    # Upper threshold on floating image
    flo_up_val = traits.Float(desc='Upper threshold value on floating image',
                              argstr='-floUpThr %f')
    # Platform to use
    platform_val = traits.Int(desc='Platform index',
                              argstr='-platf %i')
    # Platform to use
    gpuid_val = traits.Int(desc='Device to use id',
                           argstr='-gpuid %i')
    # Verbosity off
    verbosity_off_flag = traits.Bool(argstr='-voff', desc='Turn off verbose output')
    # Set the number of omp thread to use
    omp_core_val = traits.Int(desc='Number of openmp thread to use',
                              argstr='-omp %i')

    # Affine output transformation matrix file
    aff_file = File(genfile=True, desc='The output affine matrix file', argstr='-aff %s')
    # Result warped image file
    res_file = File(genfile=True, desc='The affine transformed floating image', argstr='-res %s')


class RegAladinOutputSpec(TraitedSpec):
    aff_file = File(desc='The output affine file')
    res_file = File(desc='The output transformed image')
    avg_output = traits.String(desc='Output string in the format for reg_average')


class RegAladin(NiftyRegCommand):
    _cmd = get_custom_path('reg_aladin')
    input_spec = RegAladinInputSpec
    output_spec = RegAladinOutputSpec

    def _gen_filename(self, name):
        if name == 'aff_file':
            return self._gen_fname(self.inputs.flo_file, suffix='_aff', ext='.txt')
        if name == 'res_file':
            return self._gen_fname(self.inputs.flo_file, suffix='_res', ext='.nii.gz')
        return None

    def _list_outputs(self):
        outputs = self.output_spec().get()

        if isdefined(self.inputs.aff_file):
            outputs['aff_file'] = self.inputs.aff_file
        else:
            outputs['aff_file'] = self._gen_filename('aff_file')
        if isdefined(self.inputs.res_file):
            outputs['res_file'] = self.inputs.aff_file
        else:
            outputs['res_file'] = self._gen_filename('res_file')

        # Make a list of the linear transformation file and the input image
        outputs['avg_output'] = os.path.abspath(outputs['aff_file']) + ' ' + os.path.abspath(self.inputs.flo_file)
        return outputs


class RegF3DInputSpec(CommandLineInputSpec):
    # Input reference file
    ref_file = File(exists=True, desc='The input reference/target image',
                    argstr='-ref %s', mandatory=True)
    # Input floating file
    flo_file = File(exists=True, desc='The input floating/source image',
                    argstr='-flo %s', mandatory=True)
    
    # Input Affine file
    aff_file = File(exists=True, desc='The input affine transformation file', argstr='-aff %s')

    # Input cpp file
    incpp_file = File(exists=True, desc='The input cpp transformation file', argstr='-incpp %s')
    
    # Reference mask
    rmask_file = File(exists=True, desc='Reference image mask', argstr='-rmask %s')
    
    # Smoothing kernel for reference
    ref_smooth_val = traits.Float(desc='Smoothing kernel width for reference image',
                                  argstr='-smooR %f')
    # Smoothing kernel for floating
    flo_smooth_val = traits.Float(desc='Smoothing kernel width for floating image',
                                  argstr='-smooF %f')
    
    # Lower threshold for reference image
    rlwth_thr_val = traits.Float(desc='Lower threshold for reference image',
                                 argstr='--rLwTh %f')
    # Upper threshold for reference image
    rupth_thr_val = traits.Float(desc='Upper threshold for reference image',
                                 argstr='--rUpTh %f')
    # Lower threshold for reference image
    flwth_thr_val = traits.Float(desc='Lower threshold for floating image',
                                 argstr='--fLwTh %f')
    # Upper threshold for reference image
    fupth_thr_val = traits.Float(desc='Upper threshold for floating image',
                                 argstr='--fUpTh %f')

    # Lower threshold for reference image
    rlwth2_thr_val = traits.Tuple(PositiveInt, traits.Float, 
                                  desc='Lower threshold for reference image at the specified time point',
                                  argstr='-rLwTh %d %f')
    # Upper threshold for reference image
    rupth2_thr_val = traits.Tuple(PositiveInt, traits.Float, 
                                  desc='Upper threshold for reference image at the specified time point',
                                  argstr='-rUpTh %d %f')
    # Lower threshold for reference image
    flwth2_thr_val = traits.Tuple(PositiveInt, traits.Float, 
                                  desc='Lower threshold for floating image at the specified time point',
                                  argstr='-fLwTh %d %f')
    # Upper threshold for reference image
    fupth2_thr_val = traits.Tuple(PositiveInt, traits.Float, 
                                  desc='Upper threshold for floating image at the specified time point',
                                  argstr='-fUpTh %d %f')

    # Final grid spacing along the 3 axes
    sx_val = traits.Float(desc='Final grid spacing along the x axes', argstr='-sx %f')
    sy_val = traits.Float(desc='Final grid spacing along the y axes', argstr='-sy %f')
    sz_val = traits.Float(desc='Final grid spacing along the z axes', argstr='-sz %f')

    # Regularisation options
    be_val = traits.Float(desc='Bending energy value', argstr='-be %f')
    le_val = traits.Float(desc='Linear elasticity penalty term', argstr='-le %f')
    jl_val = traits.Float(desc='Log of jacobian of deformation penalty value', argstr='-jl %f')
    no_app_jl_flag = traits.Bool(argstr='-noAppJL', 
                                 desc='Do not approximate the log of jacobian penalty at control points only')

    # Similarity measure options
    nmi_flag = traits.Bool(argstr='--nmi', desc='use NMI even when other options are specified')
    rbn_val = PositiveInt(desc='Number of bins in the histogram for reference image',
                          argstr='--rbn %d')
    fbn_val = PositiveInt(desc='Number of bins in the histogram for reference image',
                          argstr='--fbn %d')
    rbn2_val = traits.Tuple(PositiveInt, PositiveInt,
                            desc='Number of bins in the histogram for reference image for given time point',
                            argstr='-rbn %d %d')

    fbn2_val = traits.Tuple(PositiveInt, PositiveInt, 
                            desc='Number of bins in the histogram for reference image for given time point',
                            argstr='-fbn %d %d')

    lncc_val = traits.Float(desc='SD of the Gaussian for computing LNCC', argstr='--lncc %f')
    lncc2_val = traits.Tuple(PositiveInt, traits.Float, 
                             desc='SD of the Gaussian for computing LNCC for a given time point', argstr='-lncc %d %f')
    
    ssd_flag = traits.Bool(desc='Use SSD as the similarity measure', argstr='--ssd')
    ssd2_flag = PositiveInt(desc='Use SSD as the similarity measure for a given time point', 
                            argstr='-ssd %d')
    kld_flag = traits.Bool(desc='Use KL divergence as the similarity measure', argstr='--kld')
    kld2_flag = PositiveInt(desc='Use KL divergence as the similarity measure for a given time point', 
                            argstr='-kld %d')
    amc_flag = traits.Bool(desc='Use additive NMI', argstr='-amc')
    
    nox_flag = traits.Bool(desc='Don\'t optimise in x direction', argstr='-nox')
    noy_flag = traits.Bool(desc='Don\'t optimise in y direction', argstr='-noy')
    noz_flag = traits.Bool(desc='Don\'t optimise in z direction', argstr='-noz')

    # Optimization options
    maxit_val = PositiveInt(desc='Maximum number of iterations per level', argstr='-maxit %d')
    ln_val = PositiveInt(desc='Number of resolution levels to create', argstr='-ln %d')
    lp_val = PositiveInt(desc='Number of resolution levels to perform', argstr='-lp %d')
    nopy_flag = traits.Bool(desc='Do not use the multiresolution approach', argstr='-nopy')
    noconj_flag = traits.Bool(desc='Use simple GD optimization', argstr='-noConj')
    pert_val = PositiveInt(desc='Add perturbation steps after each optimization step', 
                           argstr='-pert %d')

    # F3d2 options
    vel_flag = traits.Bool(desc='Use velocity field integration', argstr='-vel')
    fmask_file = File(exists=True, desc='Floating image mask', argstr='-fmask %s')

    # Other options
    smooth_grad_val = traits.Float(desc='Kernel width for smoothing the metric gradient',
                                   argstr='-smoothGrad %f')
    # Padding value
    pad_val = traits.Float(desc='Padding value', argstr='-pad %f')
    # verbosity off
    verbosity_off_flag = traits.Bool(argstr='-voff', desc='Turn off verbose output')
    # Set the number of omp thread to use
    omp_core_val = traits.Int(desc='Number of openmp thread to use',
                              argstr='-omp %i')

    # Output CPP image file
    cpp_file = File(genfile=True, desc='The output CPP file', argstr='-cpp %s')
    # Output warped image file
    res_file = File(genfile=True, desc='The output resampled image', argstr='-res %s')


class RegF3DOutputSpec(TraitedSpec):
    cpp_file = File(desc='The output CPP file')
    res_file = File(desc='The output resampled image')
    invcpp_file = File(desc='The output inverse CPP file')
    invres_file = File(desc='The output inverse res file')
    avg_output = traits.String(desc='Output string in the format for reg_average')


class RegF3D(NiftyRegCommand):
    _cmd = get_custom_path('reg_f3d')
    input_spec = RegF3DInputSpec
    output_spec = RegF3DOutputSpec
    
    @staticmethod
    def _remove_extension(in_file):
        dn, bn, _ = split_filename(in_file)
        return os.path.join(dn, bn)

    def _gen_filename(self, name):
        if name == 'res_file':
            return self._gen_fname(self.inputs.flo_file, suffix='_res', ext='.nii.gz')
        if name == 'cpp_file':
            return self._gen_fname(self.inputs.flo_file, suffix='_cpp', ext='.nii.gz')

    def _list_outputs(self):
        outputs = self.output_spec().get()

        if isdefined(self.inputs.res_file):
            outputs['res_file'] = self.inputs.res_file
        else:
            outputs['res_file'] = self._gen_filename('res_file')

        if isdefined(self.inputs.cpp_file):
            outputs['cpp_file'] = self.inputs.cpp_file
        else:
            outputs['cpp_file'] = self._gen_filename('cpp_file')

        if self.inputs.vel_flag is True:
            outputs['invres_file'] = self._remove_extension(outputs['res_file']) + '_backward.nii.gz'
            outputs['invcpp_file'] = self._remove_extension(outputs['cpp_file']) + '_backward.nii.gz'

        # Make a list of the linear transformation file and the input image
        if self.inputs.vel_flag is True and isdefined(self.inputs.aff_file):
            outputs['avg_output'] = self.inputs.aff_file + ' ' + os.path.abspath(outputs['cpp_file']) + ' ' +\
                os.path.abspath(self.inputs.flo_file)
        else:
            outputs['avg_output'] = os.path.abspath(outputs['cpp_file']) + ' ' + os.path.abspath(self.inputs.flo_file)
        return outputs