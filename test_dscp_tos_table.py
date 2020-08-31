import pytest

from dscp_tos_table import dscp_class, kth_bit8_val, dscp_conv_tbl_row


@pytest.mark.parametrize(
    "bits_0_2, bit_3, bit_4, res_class",
    [
        (0b000, 0, 0, "cs0"),
        (0b001, 0, 1, "af11"),
        (0b011, 0, 0, "cs3"),
        (0b011, 1, 0, "af32"),
        (0b100, 1, 1, "af43"),
        (0b101, 1, 1, "ef"),
        (0b111, 0, 0, "cs7"),
    ]
)
def test_dscp_class(bits_0_2, bit_3, bit_4, res_class):
    assert dscp_class(bits_0_2, bit_3, bit_4) == res_class


@pytest.mark.parametrize(
    "byte, k_bit, bit_val",
    [
        (0b1000_0000, 0, 1),
        (0b1110_1111, 3, 0),
        (0b0100_0110, 5, 1),
        (0b0000_0001, 7, 1),
    ]
)
def test_kth_bit8_val(byte, k_bit, bit_val):
    assert kth_bit8_val(byte, k_bit) == bit_val


@pytest.mark.parametrize(
    "dscp_code, conv_row_values",
    [
        (0, ("cs0", "000000", "0x00", 0, 0, "0x00", "00000000", "000", 0, 0, 0, 0, "Routine")),
        (8, ("cs1", "001000", "0x08", 8, 32, "0x20", "00100000", "001", 1, 0, 0, 0, "Priority")),
        (12, ("af12", "001100", "0x0c", 12, 48, "0x30", "00110000", "001", 1, 1, 0, 0, "Priority")),
        (22, ("af23", "010110", "0x16", 22, 88, "0x58", "01011000", "010", 2, 1, 1, 0, "Immediate")),
        (26, ("af31", "011010", "0x1a", 26, 104, "0x68", "01101000", "011", 3, 0, 1, 0, "Flash")),
        (40, ("cs5", "101000", "0x28", 40, 160, "0xa0", "10100000", "101", 5, 0, 0, 0, "Critical")),
        (46, ("ef", "101110", "0x2e", 46, 184, "0xb8", "10111000", "101", 5, 1, 1, 0, "Critical")),
        (48, ("cs6", "110000", "0x30", 48, 192, "0xc0", "11000000", "110", 6, 0, 0, 0, "Internetwork Control")),
        (56, ("cs7", "111000", "0x38", 56, 224, "0xe0", "11100000", "111", 7, 0, 0, 0, "Network Control")),
    ]
)
def test_gen_table_row(dscp_code, conv_row_values):
    assert dscp_conv_tbl_row(dscp_code) == conv_row_values
