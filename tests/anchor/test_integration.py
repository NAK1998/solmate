from pathlib import Path

from solana.keypair import Keypair

from solmate.anchor import codegen
from podite import Static

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def test():
    keypair = Keypair.generate()
    root = str(get_project_root())
    pids = {"idl": keypair.public_key, "other": keypair.public_key}
    codegen.cli(f"{root}/tests/anchor", root, pids, "codegen", set())

    from codegen.idl.types import CallBackInfo, EnumWithFields
    from codegen.other.types.cross_idl_reference_type import CrossIdlReferenceType

    info = CallBackInfo(keypair.public_key, 129)
    _bytes = CallBackInfo.to_bytes(info)
    round_tripped = CallBackInfo.from_bytes(_bytes)
    assert info == round_tripped

    enum = EnumWithFields.HEALTH(info)
    _bytes = EnumWithFields.to_bytes(enum, format="FORMAT_BORSCH")
    round_tripped = EnumWithFields.from_bytes(_bytes)
    assert enum == round_tripped
    try:
        round_tripped = EnumWithFields.from_bytes(_bytes, format="FORMAT_ZERO_COPY")
        print(round_tripped)
        excepted = False
    except Exception:
        excepted = True
    finally:
        assert excepted

    enum = EnumWithFields.HEALTH(info)
    _bytes = EnumWithFields.to_bytes(enum, format="FORMAT_ZERO_COPY")
    round_tripped = EnumWithFields.from_bytes(_bytes)
    assert enum == round_tripped
    try:
        EnumWithFields.from_bytes(_bytes, format="FORMAT_BORSCH", checked=True)
        excepted = False
    except Exception:
        excepted = True
    finally:
        assert excepted


    reference_type = CrossIdlReferenceType(keypair.public_key, info)
    _bytes = CrossIdlReferenceType.to_bytes(reference_type)
    round_tripped = CrossIdlReferenceType.from_bytes(_bytes)
    assert reference_type == round_tripped
