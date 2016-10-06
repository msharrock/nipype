# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:


import os
from nipype.interfaces.niftyreg import (no_niftyreg, get_custom_path, RegAverage)
from nipype.testing import (assert_equal, skipif, example_data)


@skipif(no_niftyreg(cmd='reg_average'))
def test_reg_average_avg_nii():

    # Create a reg_average object
    nr = RegAverage()

    # Check if the command is properly defined
    yield assert_equal, nr.cmd, get_custom_path('reg_average')

    # Assign some input data
    one_file = example_data('im1.nii')
    two_file = example_data('im2.nii')
    three_file = example_data('im3.nii')
    nr.inputs.avg_files = [one_file, two_file, three_file]

    expected_cmd = get_custom_path('reg_average') + ' ' + os.getcwd() + os.sep + 'avg_out.nii.gz ' +\
                   '-avg ' + one_file + ' ' + two_file + ' ' + three_file
    yield assert_equal, nr.cmdline, expected_cmd


@skipif(no_niftyreg(cmd='reg_average'))
def test_reg_average_avg_txt():

    # Create a reg_average object
    nr = RegAverage()

    # Check if the command is properly defined
    yield assert_equal, nr.cmd, get_custom_path('reg_average')

    # Assign some input data
    one_file = example_data('TransformParameters.0.txt')
    two_file = example_data('ants_Affine.txt')
    three_file = example_data('elastix.txt')
    nr.inputs.avg_files = [one_file, two_file, three_file]

    expected_cmd = get_custom_path('reg_average') + ' ' + os.getcwd() + os.sep + 'avg_out.txt ' +\
                   '-avg ' + one_file + ' ' + two_file + ' ' + three_file
    yield assert_equal, nr.cmdline, expected_cmd


@skipif(no_niftyreg(cmd='reg_average'))
def test_reg_average_avg_lts():

    # Create a reg_average object
    nr = RegAverage()

    # Check if the command is properly defined
    yield assert_equal, nr.cmd, get_custom_path('reg_average')

    # Assign some input data
    one_file = example_data('TransformParameters.0.txt')
    two_file = example_data('ants_Affine.txt')
    three_file = example_data('elastix.txt')
    nr.inputs.avg_lts_files = [one_file, two_file, three_file]

    expected_cmd = get_custom_path('reg_average') + ' ' + os.getcwd() + os.sep + 'avg_out.txt ' +\
                   '-avg_lts ' + one_file + ' ' + two_file + ' ' + three_file
    yield assert_equal, nr.cmdline, expected_cmd


@skipif(no_niftyreg(cmd='reg_average'))
def test_reg_average_avg_ref():

    # Create a reg_average object
    nr = RegAverage()

    # Check if the command is properly defined
    yield assert_equal, nr.cmd, get_custom_path('reg_average')

    # Assign some input data
    ref_file = example_data('anatomical.nii')
    one_file = example_data('im1.nii')
    two_file = example_data('im2.nii')
    three_file = example_data('im3.nii')
    trans1_file = example_data('roi01.nii')
    trans2_file = example_data('roi02.nii')
    trans3_file = example_data('roi03.nii')
    nr.inputs.warp_files = [trans1_file, one_file,
                            trans2_file, two_file,
                            trans3_file, three_file]
    nr.inputs.avg_ref_file = ref_file

    expected_cmd = get_custom_path('reg_average') + ' ' + os.getcwd() + os.sep + 'avg_out.nii.gz ' +\
                   '-avg_tran ' + ref_file + ' ' + trans1_file + ' ' + one_file + ' ' +\
                   trans2_file + ' ' + two_file + ' ' + trans3_file + ' ' + three_file
    yield assert_equal, nr.cmdline, expected_cmd


@skipif(no_niftyreg(cmd='reg_average'))
def test_reg_average_demean3():

    # Create a reg_average object
    nr = RegAverage()

    # Check if the command is properly defined
    yield assert_equal, nr.cmd, get_custom_path('reg_average')

    # Assign some input data
    ref_file = example_data('anatomical.nii')
    one_file = example_data('im1.nii')
    two_file = example_data('im2.nii')
    three_file = example_data('im3.nii')
    aff1_file = example_data('TransformParameters.0.txt')
    aff2_file = example_data('ants_Affine.txt')
    aff3_file = example_data('elastix.txt')
    trans1_file = example_data('roi01.nii')
    trans2_file = example_data('roi02.nii')
    trans3_file = example_data('roi03.nii')
    nr.inputs.warp_files = [aff1_file, trans1_file, one_file,
                            aff2_file, trans2_file, two_file,
                            aff3_file, trans3_file, three_file]
    nr.inputs.demean3_ref_file = ref_file

    expected_cmd = get_custom_path('reg_average') + ' ' + os.getcwd() + os.sep + 'avg_out.nii.gz ' +\
                   '-demean3 ' + ref_file + ' ' + aff1_file + ' ' + trans1_file + ' ' + one_file + ' ' +\
                   aff2_file + ' ' + trans2_file + ' ' + two_file + ' ' +\
                   aff3_file + ' ' + trans3_file + ' ' + three_file
    yield assert_equal, nr.cmdline, expected_cmd
