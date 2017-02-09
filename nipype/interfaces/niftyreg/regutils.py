# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""The regutils module provides classes for interfacing with the `niftyreg
<http://niftyreg.sourceforge.net>`_ utility command line tools.
The interfaces were written to work with niftyreg version 1.4
"""

import warnings
import os

from ..base import TraitedSpec, File, traits, isdefined, CommandLineInputSpec
from .base import get_custom_path, NiftyRegCommand
from ...utils.filemanip import split_filename


warn = warnings.warn
warnings.filterwarnings('always', category=UserWarning)


class RegResampleInputSpec(CommandLineInputSpec):
    """ Input Spec for RegResample. """
    # Input reference file
    ref_file = File(exists=True,
                    desc='The input reference/target image',
                    argstr='-ref %s',
                    mandatory=True)
    # Input floating file
    flo_file = File(exists=True,
                    desc='The input floating/source image',
                    argstr='-flo %s',
                    mandatory=True)
    # Input deformation field
    trans_file = File(exists=True,
                      desc='The input transformation file',
                      argstr='-trans %s')

    type = traits.Enum('res', 'blank',
                       argstr='-%s',
                       position=-2,
                       usedefault=True,
                       desc='Type of output')

    # Output file name
    out_file = File(genfile=True,
                    argstr='%s',
                    position=-1,
                    desc='The output filename of the transformed image')

    # Interpolation type
    inter_val = traits.Enum('NN', 'LIN', 'CUB', 'SINC',
                            desc='Interpolation type',
                            argstr='-inter %d')

    # Padding value
    pad_val = traits.Float(desc='Padding value', argstr='-pad %f')

    # Tensor flag
    tensor_flag = traits.Bool(desc='Resample Tensor Map', argstr='-tensor ')

    # Verbosity off
    verbosity_off_flag = traits.Bool(argstr='-voff',
                                     desc='Turn off verbose output')
    # PSF flag
    desc = 'Perform the resampling in two steps to resample an image to a \
lower resolution'
    psf_flag = traits.Bool(argstr='-psf', desc=desc)
    desc = 'Minimise the matrix metric (0) or the determinant (1) when \
estimating the PSF [0]'
    psf_alg = traits.Enum(0, 1, argstr='-psf_alg %d', desc=desc)

    # Set the number of omp thread to use
    omp_core_val = traits.Int(desc='Number of openmp thread to use',
                              argstr='-omp %d')


class RegResampleOutputSpec(TraitedSpec):
    """ Output Spec for RegResample. """
    out_file = File(desc='The output filename of the transformed image')


class RegResample(NiftyRegCommand):
    """Interface for executable reg_resample from NiftyReg platform.

    Examples
    --------
    >>> from nipype.interfaces.niftyreg import RegResample
    >>> node = RegResample()
    >>> node.inputs.ref_file = 'ref.nii.gz'  # doctest: +SKIP
    >>> node.inputs.flo_file = 'flo.nii.gz'  # doctest: +SKIP
    >>> node.inputs.trans_file = 'warpfield.nii.gz'  # doctest: +SKIP
    >>> node.inputs.inter_val = 'LIN'
    >>> node.inputs.omp_core_val = 4
    >>> node.cmdline  # doctest: +SKIP
    'reg_resample -flo flo.nii.gz -inter 1 -omp 4 -ref ref.nii.gz -trans \
warpfield.nii.gz -res flo_res.nii.gz'

    """
    _cmd = get_custom_path('reg_resample')
    input_spec = RegResampleInputSpec
    output_spec = RegResampleOutputSpec

    # Need this overload to properly constraint the interpolation type input
    def _format_arg(self, name, spec, value):
        if name == 'inter_val':
            inter_val = {'NN': 0, 'LIN': 1, 'CUB': 3, 'SINC': 5}
            return spec.argstr % inter_val[value]
        else:
            return super(RegResample, self)._format_arg(name, spec, value)

    def _gen_filename(self, name):
        if name == 'out_file':
            return self._gen_fname(self.inputs.flo_file,
                                   suffix='_%s' % self.inputs.type,
                                   ext='.nii.gz')
        return None


class RegJacobianInputSpec(CommandLineInputSpec):
    """ Input Spec for RegJacobian. """
    # Reference file name
    desc = 'Reference/target file (required if specifying CPP transformations.'
    ref_file = File(exists=True,
                    desc=desc,
                    argstr='-ref %s')
    # Input transformation file
    trans_file = File(exists=True,
                      desc='The input non-rigid transformation',
                      argstr='-trans %s',
                      mandatory=True)
    type = traits.Enum('jac', 'jacL', 'jacM',
                       usedefault=True,
                       argstr='-%s',
                       position=-2,
                       desc='Type of jacobian outcome')
    out_file = File(genfile=True,
                    desc='The output jacobian determinant file name',
                    argstr='%s',
                    position=-1)
    # Set the number of omp thread to use
    omp_core_val = traits.Int(desc='Number of openmp thread to use',
                              argstr='-omp %i')


class RegJacobianOutputSpec(TraitedSpec):
    """ Output Spec for RegJacobian. """
    out_file = File(desc='The output file')


class RegJacobian(NiftyRegCommand):
    """Interface for executable reg_resample from NiftyReg platform.

    Examples
    --------
    >>> from nipype.interfaces.niftyreg import RegJacobian
    >>> node = RegJacobian()
    >>> node.inputs.ref_file = 'ref.nii.gz'  # doctest: +SKIP
    >>> node.inputs.trans_file = 'warpfield.nii.gz'  # doctest: +SKIP
    >>> node.inputs.omp_core_val = 4
    >>> node.cmdline  # doctest: +SKIP
    'reg_jacobian -omp 4 -ref ref.nii.gz -trans warpfield.nii.gz -jac \
warpfield_jac.nii.gz'

    """
    _cmd = get_custom_path('reg_jacobian')
    input_spec = RegJacobianInputSpec
    output_spec = RegJacobianOutputSpec

    def _gen_filename(self, name):
        if name == 'out_file':
            return self._gen_fname(self.inputs.trans_file,
                                   suffix='_%s' % self.inputs.type,
                                   ext='.nii.gz')
        return None


class RegToolsInputSpec(CommandLineInputSpec):
    """ Input Spec for RegTools. """
    # Input image file
    in_file = File(exists=True,
                   desc='The input image file path',
                   argstr='-in %s',
                   mandatory=True)

    # Output file path
    out_file = File(genfile=True,
                    desc='The output file name',
                    argstr='-out %s')

    # Make the output image isotropic
    iso_flag = traits.Bool(argstr='-iso', desc='Make output image isotropic')

    # Set scale, slope to 0 and 1.
    noscl_flag = traits.Bool(argstr='-noscl',
                             desc='Set scale, slope to 0 and 1')

    # Values outside the mask are set to NaN
    mask_file = File(exists=True,
                     desc='Values outside the mask are set to NaN',
                     argstr='-nan %s')

    # Threshold the input image
    desc = 'Binarise the input image with the given threshold'
    thr_val = traits.Float(desc=desc, argstr='-thr %f')

    # Binarise the input image
    bin_flag = traits.Bool(argstr='-bin', desc='Binarise the input image')

    # Compute the mean RMS between the two images
    rms_val = File(exists=True,
                   desc='Compute the mean RMS between the images',
                   argstr='-rms %s')

    # Perform division by image or value
    div_val = traits.Either(traits.Float, File(exists=True),
                            desc='Divide the input by image or value',
                            argstr='-div %s')

    # Perform multiplication by image or value
    mul_val = traits.Either(traits.Float, File(exists=True),
                            desc='Multiply the input by image or value',
                            argstr='-mul %s')

    # Perform addition by image or value
    add_val = traits.Either(traits.Float, File(exists=True),
                            desc='Add to the input image or value',
                            argstr='-add %s')

    # Perform subtraction by image or value
    sub_val = traits.Either(traits.Float, File(exists=True),
                            desc='Add to the input image or value',
                            argstr='-sub %s')

    # Downsample the image by a factor of 2.
    down_flag = traits.Bool(desc='Downsample the image by a factor of 2',
                            argstr='-down')

    # Smoothing using spline kernel
    desc = 'Smooth the input image using a cubic spline kernel'
    smo_s_val = traits.Tuple(traits.Float, traits.Float, traits.Float,
                             desc=desc,
                             argstr='-smoS %f %f %f')

    # Change the resolution of the input image
    chg_res_val = traits.Tuple(traits.Float, traits.Float, traits.Float,
                               desc='Change the resolution of the input image',
                               argstr='-chgres %f %f %f')

    # Smoothing using Gaussian kernel
    desc = 'Smooth the input image using a Gaussian kernel'
    smo_g_val = traits.Tuple(traits.Float, traits.Float, traits.Float,
                             desc=desc,
                             argstr='-smoG %f %f %f')

    # Set the number of omp thread to use
    omp_core_val = traits.Int(desc='Number of openmp thread to use',
                              argstr='-omp %i')


class RegToolsOutputSpec(TraitedSpec):
    """ Output Spec for RegTools. """
    out_file = File(desc='The output file', exists=True)


class RegTools(NiftyRegCommand):
    """Interface for executable reg_tools from NiftyReg platform.

    Examples
    --------
    >>> from nipype.interfaces.niftyreg import RegTools
    >>> node = RegTools()
    >>> node.inputs.in_file = 'im1.nii.gz'  # doctest: +SKIP
    >>> node.inputs.mul_val = 4
    >>> node.inputs.omp_core_val = 4
    >>> node.cmdline  # doctest: +SKIP
    'reg_tools -in im1.nii.gz -mul 4.0 -omp 4 -out im1_tools.nii.gz'

    """
    _cmd = get_custom_path('reg_tools')
    input_spec = RegToolsInputSpec
    output_spec = RegToolsOutputSpec
    _suffix = '_tools'


class RegAverageInputSpec(CommandLineInputSpec):
    """ Input Spec for RegAverage. """
    avg_files = traits.List(File(exist=True),
                            position=1,
                            argstr='-avg %s',
                            sep=' ',
                            xor=['avg_lts_files', 'avg_ref_file',
                                 'demean1_ref_file', 'demean2_ref_file',
                                 'demean3_ref_file', 'warp_files'],
                            desc='Averaging of images/affine transformations')

    desc = 'Robust average of affine transformations'
    avg_lts_files = traits.List(File(exist=True),
                                position=1,
                                argstr='-avg_lts %s',
                                sep=' ',
                                xor=['avg_files', 'avg_ref_file',
                                     'demean1_ref_file', 'demean2_ref_file',
                                     'demean3_ref_file', 'warp_files'],
                                desc=desc)

    desc = 'All input images are resampled into the space of <reference image>\
 and averaged. A cubic spline interpolation scheme is used for resampling'
    avg_ref_file = File(position=1,
                        argstr='-avg_tran %s',
                        xor=['avg_files', 'avg_lts_files', 'demean1_ref_file',
                             'demean2_ref_file', 'demean3_ref_file'],
                        requires=['warp_files'],
                        desc=desc)

    desc = 'Average images and demean average image that have affine \
transformations to a common space'
    demean1_ref_file = File(position=1,
                            argstr='-demean1 %s',
                            xor=['avg_files', 'avg_lts_files', 'avg_ref_file',
                                 'demean2_ref_file', 'demean3_ref_file'],
                            requires=['warp_files'],
                            desc=desc)

    desc = 'Average images and demean average image that have non-rigid \
transformations to a common space'
    demean2_ref_file = File(position=1,
                            argstr='-demean2 %s',
                            xor=['avg_files', 'avg_lts_files', 'avg_ref_file',
                                 'demean1_ref_file', 'demean3_ref_file'],
                            requires=['warp_files'],
                            desc=desc)

    desc = 'Average images and demean average image that have linear and \
non-rigid transformations to a common space'
    demean3_ref_file = File(position=1,
                            argstr='-demean3 %s',
                            xor=['avg_files', 'avg_lts_files', 'avg_ref_file',
                                 'demean1_ref_file', 'demean2_ref_file'],
                            requires=['warp_files'],
                            desc=desc)

    desc = 'transformation files and floating image pairs/triplets to the \
reference space'
    warp_files = traits.List(File(exist=True),
                             position=-1,
                             argstr='%s',
                             sep=' ',
                             xor=['avg_files', 'avg_lts_files'],
                             desc=desc)

    out_file = File(genfile=True,
                    position=0,
                    desc='Output file name',
                    argstr='%s')


class RegAverageOutputSpec(TraitedSpec):
    """ Output Spec for RegAverage. """
    out_file = File(desc='Output file name')


class RegAverage(NiftyRegCommand):
    """Interface for executable reg_average from NiftyReg platform.

    This interface is different than the others in the way that the options
    will be written in a command file that is given as a parameter.

    Examples
    --------
    >>> from nipype.interfaces.niftyreg import RegAverage
    >>> node = RegAverage()
    >>> one_file = 'im1.nii'
    >>> two_file = 'im2.nii'
    >>> three_file = 'im3.nii'
    >>> node.inputs.avg_files = [one_file, two_file, three_file]
    >>> node.cmdline
    'reg_average --cmd_file reg_average_cmd'

    """
    _cmd = get_custom_path('reg_average')
    input_spec = RegAverageInputSpec
    output_spec = RegAverageOutputSpec
    _suffix = 'avg_out'

    def _gen_filename(self, name):
        if name == 'out_file':
            if isdefined(self.inputs.avg_lts_files):
                return self._gen_fname(self._suffix, ext='.txt')
            elif isdefined(self.inputs.avg_files):
                _, _, ext = split_filename(self.inputs.avg_files[0])
                if ext not in ['.nii', '.nii.gz', '.hdr', '.img', '.img.gz']:
                    return self._gen_fname(self._suffix, ext=ext)
            return self._gen_fname(self._suffix, ext='.nii.gz')
        return None

    @property
    def cmdline(self):
        """ Rewrite the cmdline to write options in text_file."""
        argv = super(RegAverage, self).cmdline
        reg_average_cmd = os.path.join(os.getcwd(), 'reg_average_cmd')
        with open(reg_average_cmd, 'w') as f:
            f.write(argv)
        return '%s --cmd_file %s' % (self.cmd, reg_average_cmd)


class RegTransformInputSpec(CommandLineInputSpec):
    """ Input Spec for RegTransform. """
    ref1_file = File(exists=True,
                     desc='The input reference/target image',
                     argstr='-ref %s',
                     position=0)

    ref2_file = File(exists=True,
                     desc='The input second reference/target image',
                     argstr='-ref2 %s',
                     position=1,
                     requires=['ref1_file'])

    def_input = File(exists=True,
                     argstr='-def %s',
                     position=-2,
                     desc='Compute deformation field from transformation',
                     xor=['disp_input', 'flow_input', 'comp_input',
                          'upd_s_form_input', 'inv_aff_input',
                          'inv_nrr_input', 'half_input', 'make_aff_input',
                          'aff_2_rig_input', 'flirt_2_nr_input'])

    disp_input = File(exists=True,
                      argstr='-disp %s',
                      position=-2,
                      desc='Compute displacement field from transformation',
                      xor=['def_input', 'flow_input', 'comp_input',
                           'upd_s_form_input', 'inv_aff_input',
                           'inv_nrr_input', 'half_input', 'make_aff_input',
                           'aff_2_rig_input', 'flirt_2_nr_input'])

    flow_input = File(exists=True,
                      argstr='-flow %s',
                      position=-2,
                      desc='Compute flow field from spline SVF',
                      xor=['def_input', 'disp_input', 'comp_input',
                           'upd_s_form_input', 'inv_aff_input',
                           'inv_nrr_input', 'half_input', 'make_aff_input',
                           'aff_2_rig_input', 'flirt_2_nr_input'])

    comp_input = File(exists=True,
                      argstr='-comp %s',
                      position=-3,
                      desc='compose two transformations',
                      xor=['def_input', 'disp_input', 'flow_input',
                           'upd_s_form_input', 'inv_aff_input',
                           'inv_nrr_input', 'half_input', 'make_aff_input',
                           'aff_2_rig_input', 'flirt_2_nr_input'],
                      requires=['comp_input2'])

    comp_input2 = File(exists=True,
                       argstr='%s',
                       position=-2,
                       desc='compose two transformations')

    desc = 'Update s-form using the affine transformation'
    upd_s_form_input = File(exists=True,
                            argstr='-updSform %s',
                            position=-3,
                            desc=desc,
                            xor=['def_input', 'disp_input', 'flow_input',
                                 'comp_input', 'inv_aff_input',
                                 'inv_nrr_input', 'half_input',
                                 'make_aff_input', 'aff_2_rig_input',
                                 'flirt_2_nr_input'],
                            requires=['upd_s_form_input2'])

    desc = 'Update s-form using the affine transformation'
    upd_s_form_input2 = File(exists=True,
                             argstr='%s',
                             position=-2,
                             desc=desc,
                             requires=['upd_s_form_input'])

    inv_aff_input = File(exists=True,
                         argstr='-invAff %s',
                         position=-2,
                         desc='Invert an affine transformation',
                         xor=['def_input', 'disp_input', 'flow_input',
                              'comp_input', 'upd_s_form_input',
                              'inv_nrr_input', 'half_input', 'make_aff_input',
                              'aff_2_rig_input', 'flirt_2_nr_input'])

    inv_nrr_input = traits.Tuple(File(exists=True), File(exists=True),
                                 desc='Invert a non-linear transformation',
                                 argstr='-invNrr %s %s',
                                 position=-2,
                                 xor=['def_input', 'disp_input', 'flow_input',
                                      'comp_input', 'upd_s_form_input',
                                      'inv_aff_input', 'half_input',
                                      'make_aff_input', 'aff_2_rig_input',
                                      'flirt_2_nr_input'])

    half_input = File(exists=True,
                      argstr='-half %s',
                      position=-2,
                      desc='Half way to the input transformation',
                      xor=['def_input', 'disp_input', 'flow_input',
                           'comp_input', 'upd_s_form_input',
                           'inv_aff_input', 'inv_nrr_input', 'make_aff_input',
                           'aff_2_rig_input', 'flirt_2_nr_input'])

    argstr_tmp = '-makeAff %f %f %f %f %f %f %f %f %f %f %f %f'
    make_aff_input = traits.Tuple(traits.Float, traits.Float, traits.Float,
                                  traits.Float, traits.Float, traits.Float,
                                  traits.Float, traits.Float, traits.Float,
                                  traits.Float, traits.Float, traits.Float,
                                  argstr=argstr_tmp,
                                  position=-2,
                                  desc='Make an affine transformation matrix',
                                  xor=['def_input', 'disp_input', 'flow_input',
                                       'comp_input', 'upd_s_form_input',
                                       'inv_aff_input', 'inv_nrr_input',
                                       'half_input', 'aff_2_rig_input',
                                       'flirt_2_nr_input'])

    desc = 'Extract the rigid component from affine transformation'
    aff_2_rig_input = File(exists=True,
                           argstr='-aff2rig %s',
                           position=-2,
                           desc=desc,
                           xor=['def_input', 'disp_input', 'flow_input',
                                'comp_input', 'upd_s_form_input',
                                'inv_aff_input', 'inv_nrr_input', 'half_input',
                                'make_aff_input', 'flirt_2_nr_input'])

    desc = 'Convert a FLIRT affine transformation to niftyreg affine \
transformation'
    flirt_2_nr_input = traits.Tuple(File(exists=True), File(exists=True),
                                    File(exists=True),
                                    argstr='-flirtAff2NR %s %s %s',
                                    position=-2,
                                    desc=desc,
                                    xor=['def_input', 'disp_input',
                                         'flow_input', 'comp_input',
                                         'upd_s_form_input', 'inv_aff_input',
                                         'inv_nrr_input', 'half_input',
                                         'make_aff_input', 'aff_2_rig_input'])

    out_file = File(genfile=True,
                    position=-1,
                    argstr='%s',
                    desc='transformation file to write')

    # Set the number of omp thread to use
    omp_core_val = traits.Int(desc='Number of openmp thread to use',
                              argstr='-omp %i')


class RegTransformOutputSpec(TraitedSpec):
    """ Output Spec for RegTransform. """
    desc = 'Output File (transformation in any format)'
    out_file = File(exists=True, desc=desc)


class RegTransform(NiftyRegCommand):
    """Interface for executable reg_transform from NiftyReg platform.

    Examples
    --------
    >>> from nipype.interfaces.niftyreg import RegResample
    >>> node = RegTransform()
    >>> node.inputs.def_input = 'warpfield.nii'
    >>> node.inputs.omp_core_val = 4
    >>> node.cmdline  # doctest: +SKIP
    'reg_transform -omp 4 -def warpfield.nii warpfield_trans.nii.gz'

    """
    _cmd = get_custom_path('reg_transform')
    input_spec = RegTransformInputSpec
    output_spec = RegTransformOutputSpec
    _suffix = '_trans'

    def _find_input(self):
        inputs = [self.inputs.def_input, self.inputs.disp_input,
                  self.inputs.flow_input, self.inputs.comp_input,
                  self.inputs.comp_input2, self.inputs.upd_s_form_input,
                  self.inputs.inv_aff_input, self.inputs.inv_nrr_input,
                  self.inputs.half_input, self.inputs.make_aff_input,
                  self.inputs.aff_2_rig_input, self.inputs.flirt_2_nr_input]
        entries = []
        for entry in inputs:
            if isdefined(entry):
                entries.append(entry)
                _, _, ext = split_filename(entry)
                if ext == '.nii' or ext == '.nii.gz' or ext == '.hdr':
                    return entry
        if len(entries):
            return entries[0]
        return None

    def _gen_filename(self, name):
        if name == 'out_file':
            if isdefined(self.inputs.make_aff_input):
                return self._gen_fname('matrix', suffix=self._suffix,
                                       ext='.txt')

            if isdefined(self.inputs.comp_input) and \
               isdefined(self.inputs.comp_input2):
                _, bn1, ext1 = split_filename(self.inputs.comp_input)
                _, _, ext2 = split_filename(self.inputs.comp_input2)
                if ext1 in ['.nii', '.nii.gz', '.hdr', '.img', '.img.gz'] or \
                   ext2 in ['.nii', '.nii.gz', '.hdr', '.img', '.img.gz']:
                    return self._gen_fname(bn1, suffix=self._suffix,
                                           ext='.nii.gz')
                else:
                    return self._gen_fname(bn1, suffix=self._suffix, ext=ext1)

            if isdefined(self.inputs.flirt_2_nr_input):
                return self._gen_fname(self.inputs.flirt_2_nr_input[0],
                                       suffix=self._suffix, ext='.txt')

            input_to_use = self._find_input()
            _, _, ext = split_filename(input_to_use)
            if ext not in ['.nii', '.nii.gz', '.hdr', '.img', '.img.gz']:
                return self._gen_fname(input_to_use, suffix=self._suffix,
                                       ext=ext)
            else:
                return self._gen_fname(input_to_use, suffix=self._suffix,
                                       ext='.nii.gz')

        return None

    def _list_outputs(self):
        outputs = self.output_spec().get()

        if isdefined(self.inputs.out_file):
            outputs['out_file'] = self.inputs.out_file
        else:
            outputs['out_file'] = self._gen_filename('out_file')

        return outputs


class RegMeasureInputSpec(CommandLineInputSpec):
    """ Input Spec for RegMeasure. """
    # Input reference file
    ref_file = File(exists=True,
                    desc='The input reference/target image',
                    argstr='-ref %s',
                    mandatory=True)
    # Input floating file
    flo_file = File(exists=True,
                    desc='The input floating/source image',
                    argstr='-flo %s',
                    mandatory=True)
    measure_type = traits.Enum('ncc', 'lncc', 'nmi', 'ssd',
                               mandatory=True,
                               argstr='-%s',
                               desc='Measure of similarity to compute')
    out_file = File(genfile=True,
                    argstr='-out %s',
                    desc='The output text file containing the measure')
    # Set the number of omp thread to use
    omp_core_val = traits.Int(desc='Number of openmp thread to use',
                              argstr='-omp %i')


class RegMeasureOutputSpec(TraitedSpec):
    """ Output Spec for RegMeasure. """
    out_file = File(desc='The output text file containing the measure')


class RegMeasure(NiftyRegCommand):
    """Interface for executable reg_measure from NiftyReg platform.

    Examples
    --------
    >>> from nipype.interfaces.niftyreg import RegMeasure
    >>> node = RegMeasure()
    >>> node.inputs.ref_file = 'im1.nii'  # doctest: +SKIP
    >>> node.inputs.flo_file = 'im2.nii'  # doctest: +SKIP
    >>> node.inputs.measure_type = 'lncc'
    >>> node.inputs.omp_core_val = 4
    >>> node.cmdline  # doctest: +SKIP
    'reg_measure -flo {flo} -lncc -omp 4 -out {out} -ref {ref}'

    """
    _cmd = get_custom_path('reg_measure')
    input_spec = RegMeasureInputSpec
    output_spec = RegMeasureOutputSpec

    def _gen_filename(self, name):
        if name == 'out_file':
            return self._gen_fname(self.inputs.flo_file,
                                   suffix='_%s' % self.inputs.measure_type,
                                   ext='.txt')
        return None
