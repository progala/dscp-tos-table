import csv
from pathlib import Path


TOS_STRING_TBL = {
    0: "Routine",
    1: "Priority",
    2: "Immediate",
    3: "Flash",
    4: "FlashOverride",
    5: "Critical",
    6: "Internetwork Control",
    7: "Network Control",
}


def dscp_class(bits_0_2, bit_3, bit_4):
    """
    Takes values of DSCP bits and computes dscp class

    Bits 0-2 decide major class
    Bit 3-4 decide drop precedence

    :param bits_0_2: int: decimal value of bits 0-2
    :param bit_3: int: value of bit 3
    :param bit_4: int: value of bit 4
    :return: DSCP class name
    """
    bits_3_4 = (bit_3 << 1) + bit_4
    if bits_3_4 == 0:
        dscp_cl = "cs{}".format(bits_0_2)
    elif (bits_0_2, bits_3_4) == (5, 3):
        dscp_cl = "ef"
    else:
        dscp_cl = "af{}{}".format(bits_0_2, bits_3_4)

    return dscp_cl


def kth_bit8_val(byte, k):
    """
    Returns value of k-th bit

    Most Significant Bit, bit-0, on the Left

    :param byte: 8 bit integer to check
    :param k: bit value to return
    :return: 1 if bit is set, 0 if not
    """
    return 1 if byte & (0b1000_0000 >> k) else 0


def dscp_conv_tbl_row(dscp):
    """
    Generates DSCP to ToS conversion values as well as different representations

    :param dscp: int: decimal DSCP code
    :return: dict with each value assigned to value name
    """
    tos_dec = dscp << 2
    tos_bin = "{:08b}".format(tos_dec)
    tos_prec_bin = tos_bin[0:3]
    tos_prec_dec = int(tos_prec_bin, 2)
    tos_del_fl = kth_bit8_val(tos_dec, 3)
    tos_thr_fl = kth_bit8_val(tos_dec, 4)
    tos_rel_fl = kth_bit8_val(tos_dec, 5)
    dscp_cl = dscp_class(tos_prec_dec, tos_del_fl, tos_thr_fl)

    tbl_row_vals = (
        dscp_cl,
        "{:06b}".format(dscp),
        "{:#04x}".format(dscp),
        dscp,
        tos_dec,
        "{:#04x}".format(tos_dec),
        tos_bin,
        tos_prec_bin,
        tos_prec_dec,
        tos_del_fl,
        tos_thr_fl,
        tos_rel_fl,
        TOS_STRING_TBL[tos_prec_dec],
    )

    return tbl_row_vals


def gen_dscp_conversion_table():
    """
    Generates DSCP to TOS conversion table with rows for selected DSCP codes

    Final table is a list of dictionaries to make writing CSV easier

    :return: list(dict): final DSCP to TOS conversion table
    """
    column_names = (
        "DSCP Class",
        "DSCP (bin)",
        "DSCP (hex)",
        "DSCP (dec)",
        "ToS (dec)",
        "ToS (hex)",
        "ToS (bin)",
        "ToS Prec. (bin)",
        "ToS Prec. (dec)",
        "ToS Delay Flag",
        "ToS Throughput Flag",
        "ToS Reliability Flag",
        "TOS String Format",
    )
    # These are the DSCP codes we're interested in
    dscps_dec = (0, *range(8, 41, 2), 46, 48, 56)

    conv_tbl = [dict(zip(column_names, dscp_conv_tbl_row(dscp))) for dscp in dscps_dec]

    return conv_tbl


def main():
    dscp_conversion_table = gen_dscp_conversion_table()

    with Path("dscp_tos_conv_table.csv").open(mode="w", newline="") as fout:
        dict_writer = csv.DictWriter(f=fout, fieldnames=dscp_conversion_table[0].keys())

        dict_writer.writeheader()
        dict_writer.writerows(dscp_conversion_table)


if __name__ == "__main__":
    main()
