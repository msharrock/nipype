# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ....testing import assert_equal
from ..regutils import RegJacobian


def test_RegJacobian_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    omp_core_val=dict(argstr='-omp %i',
    ),
    out_file=dict(argstr='%s',
    genfile=True,
    position=-1,
    ),
    ref_file=dict(argstr='-ref %s',
    ),
    terminal_output=dict(nohash=True,
    ),
    trans_file=dict(argstr='-trans %s',
    mandatory=True,
    ),
    type=dict(argstr='-%s',
    position=-2,
    usedefault=True,
    ),
    )
    inputs = RegJacobian.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            yield assert_equal, getattr(inputs.traits()[key], metakey), value


def test_RegJacobian_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = RegJacobian.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            yield assert_equal, getattr(outputs.traits()[key], metakey), value
