# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ..dwi import DwiTool


def test_DwiTool_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    b0_file=dict(argstr='-b0 %s',
    mandatory=True,
    ),
    ball_flag=dict(argstr='-ball',
    xor=['mono_flag', 'ivim_flag', 'dti_flag', 'dti_flag2', 'ballv_flag', 'nod_flag', 'nodv_flag'],
    ),
    ballv_flag=dict(argstr='-ballv',
    xor=['mono_flag', 'ivim_flag', 'dti_flag', 'dti_flag2', 'ball_flag', 'nod_flag', 'nodv_flag'],
    ),
    bval_file=dict(argstr='-bval %s',
    mandatory=True,
    ),
    bvec_file=dict(argstr='-bvec %s',
    mandatory=True,
    ),
    diso_val=dict(argstr='-diso %f',
    ),
    dpr_val=dict(argstr='-dpr %f',
    ),
    dti_flag=dict(argstr='-dti',
    xor=['mono_flag', 'ivim_flag', 'dti_flag2', 'ball_flag', 'ballv_flag', 'nod_flag', 'nodv_flag'],
    ),
    dti_flag2=dict(argstr='-dti2',
    xor=['mono_flag', 'ivim_flag', 'dti_flag', 'ball_flag', 'ballv_flag', 'nod_flag', 'nodv_flag'],
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    famap_file=dict(argstr='-famap %s',
    genfile=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    ivim_flag=dict(argstr='-ivim',
    xor=['mono_flag', 'dti_flag', 'dti_flag2', 'ball_flag', 'ballv_flag', 'nod_flag', 'nodv_flag'],
    ),
    logdti_file=dict(argstr='-logdti2 %s',
    genfile=True,
    requires=['dti_flag'],
    ),
    mask_file=dict(argstr='-mask %s',
    mandatory=True,
    ),
    mcmap_file=dict(argstr='-mcmap %s',
    genfile=True,
    ),
    mdmap_file=dict(argstr='-mdmap %s',
    genfile=True,
    ),
    mono_flag=dict(argstr='-mono',
    xor=['ivim_flag', 'dti_flag', 'dti_flag2', 'ball_flag', 'ballv_flag', 'nod_flag', 'nodv_flag'],
    ),
    nod_flag=dict(argstr='-nod',
    xor=['mono_flag', 'ivim_flag', 'dti_flag', 'dti_flag2', 'ball_flag', 'ballv_flag', 'nodv_flag'],
    ),
    nodv_flag=dict(argstr='-nodv',
    xor=['mono_flag', 'ivim_flag', 'dti_flag', 'dti_flag2', 'ball_flag', 'ballv_flag', 'nod_flag'],
    ),
    op_basename=dict(usedefault=True,
    ),
    rgbmap_file=dict(argstr='-rgbmap %s',
    genfile=True,
    requires=['dti_flag'],
    ),
    source_file=dict(argstr='-source %s',
    mandatory=True,
    ),
    syn_file=dict(argstr='-syn %s',
    genfile=True,
    ),
    terminal_output=dict(nohash=True,
    ),
    v1map_file=dict(argstr='-v1map %s',
    genfile=True,
    ),
    )
    inputs = DwiTool.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_DwiTool_outputs():
    output_map = dict(famap_file=dict(),
    logdti_file=dict(),
    mcmap_file=dict(),
    mdmap_file=dict(),
    rgbmap_file=dict(),
    syn_file=dict(),
    v1map_file=dict(),
    )
    outputs = DwiTool.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
