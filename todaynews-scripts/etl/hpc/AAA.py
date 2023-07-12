import sys
import pymysql
import pandas as pd
import time
import numpy


list1 = [
    1007,
    103,
    1054,
    1055,
    1063,
    1079,
    1080,
    1084,
    1097,
    1098,
    1099,
    1100,
    1101,
    1102,
    1105,
    1108,
    1111,
    1112,
    1113,
    1117,
    112,
    1121,
    1122,
    1128,
    1129,
    1131,
    118,
    1183,
    1184,
    1185,
    1195,
    1217,
    1224,
    1225,
    1226,
    1230,
    1236,
    1287,
    1296,
    1303,
    1318,
    1330,
    1374,
    1378,
    1391,
    140,
    1409,
    141,
    1410,
    142,
    1434,
    1439,
    144,
    1449,
    146,
    1463,
    147,
    1473,
    1516,
    1517,
    1530,
    1536,
    1540,
    1543,
    1562,
    1563,
    1564,
    1565,
    1566,
    1576,
    1579,
    158,
    1586,
    1589,
    1591,
    1594,
    1599,
    1609,
    1611,
    1620,
    1627,
    165,
    1652,
    1653,
    1669,
    1690,
    1696,
    1707,
    1761,
    1766,
    1786,
    1789,
    1791,
    1813,
    1820,
    1826,
    185,
    187,
    1881,
    1889,
    1890,
    1891,
    1892,
    1893,
    191,
    1912,
    1914,
    1916,
    1918,
    193,
    1936,
    195,
    1955,
    1959,
    1960,
    1977,
    1999,
    2001,
    2002,
    2010,
    2011,
    2017,
    2020,
    2023,
    2032,
    2036,
    2038,
    2081,
    2082,
    2113,
    2114,
    2127,
    2139,
    2142,
    2143,
    2162,
    2164,
    2171,
    2172,
    2174,
    2181,
    2184,
    2187,
    22,
    2202,
    2207,
    221,
    2224,
    2225,
    2226,
    2256,
    2296,
    231,
    2316,
    2317,
    232,
    2329,
    234,
    2345,
    2358,
    2359,
    2378,
    24,
    2411,
    2416,
    242,
    2458,
    25,
    2522,
    254,
    2547,
    255,
    2585,
    2668,
    273,
    2744,
    2749,
    2788,
    2794,
    2795,
    2827,
    293,
    2966,
    3015,
    3035,
    310,
    312,
    313,
    3130,
    3134,
    3137,
    3139,
    314,
    3142,
    3144,
    3145,
    3148,
    315,
    3152,
    3153,
    3154,
    3155,
    3157,
    3158,
    318,
    320,
    3206,
    324,
    3241,
    328,
    3283,
    329,
    3296,
    3297,
    3298,
    3299,
    330,
    3300,
    3301,
    3302,
    3303,
    332,
    333,
    336,
    338,
    3381,
    3392,
    341,
    343,
    344,
    345,
    347,
    3474,
    3477,
    351,
    352,
    353,
    354,
    3581,
    3582,
    3589,
    3591,
    3621,
    363,
    3634,
    3640,
    3642,
    365,
    373,
    3749,
    375,
    3781,
    3782,
    3809,
    3810,
    3814,
    3817,
    3822,
    3829,
    3840,
    3844,
    3849,
    3852,
    3878,
    3891,
    3902,
    3903,
    3918,
    3919,
    397,
    3977,
    3978,
    3990,
    3991,
    4038,
    4056,
    4058,
    4063,
    4064,
    4068,
    4070,
    409,
    410,
    4105,
    4124,
    4126,
    428,
    4432,
    444,
    4443,
    445,
    4485,
    4487,
    451,
    4621,
    4622,
    4629,
    4630,
    476,
    4823,
    4824,
    4825,
    4826,
    4832,
    4840,
    4851,
    486,
    4875,
    4915,
    4918,
    493,
    4932,
    4942,
    4943,
    496,
    4994,
    4995,
    500,
    5020,
    5026,
    5075,
    5099,
    5102,
    5123,
    519,
    521,
    5213,
    5216,
    5220,
    523,
    5246,
    525,
    5259,
    529,
    5291,
    530,
    5304,
    5305,
    5310,
    5312,
    5319,
    5325,
    5330,
    5331,
    5332,
    5373,
    5377,
    5380,
    5396,
    5397,
    5398,
    5482,
    5494,
    5498,
    5514,
    5541,
    5549,
    5552,
    5557,
    5560,
    5569,
    5570,
    5612,
    5614,
    5624,
    5625,
    5626,
    5627,
    5629,
    5637,
    565,
    5652,
    566,
    5666,
    567,
    568,
    5696,
    570,
    5707,
    5733,
    5747,
    576,
    5763,
    5781,
    5783,
    5784,
    5815,
    5816,
    5818,
    582,
    583,
    584,
    5840,
    5852,
    5853,
    5890,
    5955,
    5957,
    596,
    597,
    5988,
    6004,
    6008,
    6009,
    6010,
    6012,
    6013,
    6016,
    6017,
    602,
    6035,
    6036,
    6040,
    6041,
    6042,
    6043,
    6045,
    608,
    6101,
    6106,
    6119,
    6135,
    6140,
    6156,
    6157,
    6170,
    6171,
    6172,
    6173,
    6174,
    6175,
    6176,
    6177,
    6178,
    6180,
    6183,
    6185,
    6187,
    6194,
    6195,
    6196,
    6207,
    6208,
    6210,
    6214,
    6240,
    6241,
    6242,
    6252,
    6253,
    6261,
    6262,
    6263,
    6266,
    628,
    6296,
    63,
    6345,
    6346,
    6347,
    6387,
    6388,
    655,
    6673,
    6674,
    6675,
    6742,
    6743,
    6744,
    6823,
    6824,
    6825,
    6838,
    6839,
    6840,
    6849,
    6889,
    6890,
    7014,
    7015,
    7016,
    7017,
    7018,
    7019,
    7032,
    7033,
    7034,
    706,
    7113,
    7114,
    7140,
    7141,
    717,
    7173,
    7174,
    7223,
    7284,
    7285,
    7321,
    7322,
    7348,
    7392,
    7397,
    7398,
    7399,
    7400,
    7401,
    7402,
    7409,
    7424,
    7429,
    7438,
    7457,
    7459,
    7513,
    7514,
    7515,
    7517,
    7518,
    7522,
    7524,
    7525,
    7571,
    7625,
    7647,
    7652,
    7653,
    7659,
    7660,
    7661,
    7662,
    7663,
    7680,
    7688,
    7689,
    7696,
    7697,
    7698,
    7700,
    7701,
    7702,
    7703,
    7704,
    7705,
    7707,
    7708,
    7709,
    7711,
    7712,
    7718,
    7719,
    7720,
    7721,
    7722,
    7723,
    7725,
    7727,
    7729,
    7730,
    7731,
    7744,
    7745,
    7747,
    7748,
    7749,
    7750,
    7752,
    7753,
    7754,
    7755,
    7756,
    7757,
    7759,
    7760,
    7761,
    7762,
    7763,
    7764,
    7766,
    7767,
    7769,
    7770,
    7771,
    7772,
    7773,
    7775,
    7776,
    7777,
    7778,
    7779,
    7780,
    7782,
    7784,
    7785,
    7788,
    7789,
    7790,
    7792,
    7793,
    7795,
    7796,
    7797,
    7799,
    7800,
    7801,
    7802,
    7804,
    7806,
    7809,
    7810,
    7814,
    7815,
    7816,
    7817,
    7818,
    7819,
    7820,
    7821,
    7822,
    7824,
    7825,
    7826,
    7827,
    7828,
    7829,
    7832,
    7834,
    7835,
    7837,
    7838,
    7839,
    7840,
    7841,
    7843,
    7844,
    7845,
    7846,
    7847,
    7848,
    7850,
    7853,
    7854,
    7855,
    7856,
    7858,
    7859,
    7861,
    7863,
    7864,
    7865,
    7866,
    7867,
    7868,
    7869,
    7871,
    7872,
    7873,
    7874,
    7875,
    7876,
    7879,
    7880,
    7881,
    7882,
    7883,
    7884,
    7885,
    7886,
    7889,
    7890,
    7891,
    7892,
    7893,
    7894,
    7897,
    7898,
    7900,
    7901,
    7902,
    7903,
    7904,
    7906,
    7907,
    7908,
    7909,
    7910,
    7912,
    7913,
    7914,
    7915,
    7916,
    7917,
    7918,
    7919,
    7920,
    7922,
    7923,
    7924,
    7925,
    7926,
    7927,
    7929,
    7931,
    7934,
    7935,
    7936,
    7937,
    7938,
    7939,
    7942,
    7943,
    7944,
    7945,
    7946,
    7947,
    7949,
    7950,
    7952,
    7953,
    7956,
    7957,
    7963,
    7964,
    7966,
    7967,
    7968,
    7970,
    7973,
    7974,
    7975,
    7976,
    7980,
    7981,
    7984,
    7986,
    7987,
    7988,
    7996,
    7997,
    8005,
    8012,
    8013,
    8017,
    8018,
    8020,
    8029,
    8053,
    8057,
    8068,
    8072,
    8075,
    8077,
    8086,
    8087,
    8091,
    8098,
    8099,
    8122,
    8124,
    8127,
    815,
    8171,
    8175,
    8179,
    8181,
    8183,
    8184,
    8206,
    8209,
    8216,
    8217,
    822,
    8245,
    8247,
    8248,
    8249,
    8250,
    8251,
    8252,
    8253,
    8255,
    8256,
    8258,
    8260,
    8262,
    8264,
    8269,
    8271,
    8272,
    8274,
    8276,
    8277,
    8280,
    8281,
    8282,
    8284,
    8287,
    8289,
    8290,
    8293,
    8294,
    8295,
    8296,
    8297,
    8299,
    830,
    8302,
    8303,
    8304,
    8305,
    8306,
    8325,
    8326,
    8327,
    8332,
    8333,
    8336,
    8337,
    8338,
    8340,
    8341,
    8342,
    8343,
    8344,
    8347,
    8350,
    8351,
    8352,
    8354,
    8357,
    8360,
    8361,
    8364,
    8366,
    8367,
    8370,
    8371,
    8372,
    8374,
    8376,
    8383,
    8384,
    8385,
    8386,
    8388,
    8389,
    839,
    8390,
    8392,
    8393,
    8395,
    8399,
    8401,
    8402,
    8411,
    8413,
    8415,
    8425,
    8426,
    843,
    8450,
    8451,
    8453,
    8454,
    8457,
    8460,
    8461,
    8462,
    8478,
    8479,
    8480,
    8481,
    8482,
    8483,
    8484,
    8485,
    8486,
    8487,
    8497,
    8512,
    8514,
    855,
    8553,
    8557,
    8592,
    8614,
    8623,
    8635,
    865,
    8659,
    8660,
    8672,
    8675,
    8676,
    8681,
    8682,
    8683,
    8685,
    8689,
    8690,
    8693,
    8715,
    8718,
    8720,
    8727,
    8734,
    8739,
    8745,
    8746,
    8747,
    8749,
    8752,
    8753,
    8755,
    8757,
    8758,
    8760,
    8773,
    8774,
    8777,
    8779,
    8781,
    8784,
    8786,
    8788,
    8790,
    8792,
    8794,
    8797,
    8799,
    8801,
    8803,
    8804,
    8810,
    8811,
    8812,
    8813,
    8815,
    8831,
    8832,
    8833,
    8834,
    8835,
    8848,
    8849,
    8856,
    8857,
    8858,
    8859,
    8883,
    8884,
    8887,
    8891,
    8892,
    8893,
    8894,
    8895,
    8916,
    8922,
    8934,
    8936,
    8945,
    8947,
    8978,
    8985,
    9008,
    9010,
    9013,
    9018,
    9036,
    9037,
    9054,
    9059,
    9060,
    9061,
    9062,
    9063,
    9064,
    9065,
    9066,
    9067,
    9068,
    9071,
    9077,
    9081,
    9087,
    9088,
    9090,
    9133,
    9135,
    9138,
    9172,
    9173,
    9195,
    9196,
    9209,
    9210,
    9211,
    9212,
    9213,
    9214,
    9294,
    9371,
    9387,
    9526,
    9536,
    9548,
    9550,
    9723,
    9742,
    9755,
    9898,
    9899
]

list2 = [
    4063,
    4068,
    4124,
    4064,
    4126,
    8788,
    8786,
    4070,
    165,
    3134,
    3155,
    3154,
    3153,
    3157,
    3152,
    3137,
    3130,
    500,
    7843,
    6214,
    4629,
    4621,
    8592,
    8557,
    8553,
    8715,
    8690,
    8659,
    8352,
    8364,
    8361,
    8360,
    8343,
    8342,
    8341,
    8340,
    8338,
    8337,
    8336,
    8351,
    8350,
    8347,
    8344,
    8327,
    8326,
    8325,
    8333,
    8332,
    8303,
    8302,
    8277,
    8276,
    8274,
    8272,
    8262,
    8260,
    8258,
    8256,
    8271,
    8264,
    8454,
    8457,
    8426,
    8425,
    8247,
    8255,
    8249,
    8248,
    7847,
    7844,
    7841,
    7840,
    7848,
    7829,
    7828,
    7827,
    7826,
    7825,
    7824,
    7839,
    7838,
    7837,
    7835,
    7834,
    7832,
    7815,
    7814,
    7810,
    7809,
    7822,
    7821,
    7820,
    7819,
    7817,
    7816,
    7799,
    7797,
    7796,
    7795,
    7792,
    7806,
    7804,
    7802,
    7801,
    7800,
    7782,
    7780,
    7779,
    7778,
    7777,
    7776,
    7790,
    7789,
    7788,
    7785,
    7784,
    7767,
    7766,
    7764,
    7763,
    7762,
    7761,
    7760,
    7775,
    7773,
    7772,
    7771,
    7770,
    7769,
    7750,
    7748,
    7747,
    7745,
    7744,
    7759,
    7757,
    7756,
    7755,
    7754,
    7753,
    7752,
    9036,
    9213,
    9211,
    9209,
    9195,
    8895,
    8892,
    8848,
    8833,
    8831,
    6252,
    6387,
    6036,
    6017,
    6009,
    6157,
    5816,
    5853,
    7517,
    7515,
    7514,
    7513,
    7284,
    7409,
    7173,
    7140,
    6889,
    3977,
    5560,
    5549,
    5666,
    5570,
    5305,
    4994,
    4826,
    4824,
    2113,
    2358,
    2359,
    1889,
    1766,
    3589,
    2788,
    445,
    409,
    191,
    195,
    25,
    1079,
    1054,
    8289,
    7880,
    8623,
    4622,
    8718,
    8635,
    7920,
    2207,
    7885,
    8614,
    8374,
    8660,
    8399,
    8384,
    7906,
    8372,
    4630,
    7942,
    5733,
    2522,
    8395,
    8370,
    8383,
    7949,
    2187,
    8366,
    8401,
    8371,
    8402,
    8487,
    655,
    8392,
    8389,
    8386,
    8390,
    8305,
    8376,
    8296,
    8282,
    8287,
    8281,
    8461,
    8252,
    7858,
    8251,
    8385,
    7867,
    7881,
    8304,
    7936,
    7855,
    7861,
    8297,
    7931,
    8299,
    8290,
    7850,
    8280,
    7845,
    8250,
    7944,
    7882,
    7859,
    7864,
    2202,
    7950,
    7935,
    7927,
    7873,
    7937,
    7952,
    7910,
    8393,
    7943,
    3990,
    7953,
    8388,
    7923,
    7917,
    7894,
    8293,
    7890,
    7908,
    7914,
    7918,
    6840,
    6187,
    7016,
    6196,
    6825,
    7034,
    6180,
    7019,
    7934,
    7900,
    7907,
    7939,
    7902,
    5312,
    2184,
    7903,
    7893,
    7879,
    7876,
    7884,
    7872,
    9755,
    2416,
    7891,
    7904,
    7869,
    7924,
    7919,
    7957,
    7866,
    7926,
    7916,
    7947,
    7929,
    7956,
    7856,
    7883,
    7889,
    9214,
    7854,
    9196,
    7922,
    9210,
    7865,
    7886,
    8832,
    8834,
    6388,
    6016,
    6008,
    9212,
    7909,
    6296,
    5815,
    7853,
    6253,
    6035,
    5852,
    3978,
    7912,
    103,
    7174,
    4825,
    5304,
    7285,
    7141,
    1890,
    8453,
    142,
    63,
    444,
    410,
    193,
    7938,
    221,
    1055,
    1080,
    5569,
    8720,
    4823,
    324,
    5552,
    8849,
    6890,
    8497,
    6040,
    7846,
    8462,
    9387,
    9371,
    3621,
    8253,
    7424,
    7871,
    6838,
    6823,
    6194,
    6183,
    7014,
    7017,
    8685,
    6173,
    6172,
    6171,
    6170,
    7032,
    7968,
    5627,
    7913,
    8354,
    7980,
    4487,
    4485,
    2164,
    566,
    7976,
    7963,
    525,
    9536,
    1226,
    8451,
    7987,
    2345,
    1230,
    5988,
    7984,
    7897,
    2458,
    234,
    8295,
    2668,
    830,
    7874,
    5763,
    1892,
    7975,
    7997,
    8747,
    7986,
    6824,
    6185,
    8693,
    6175,
    7793,
    5514,
    6174,
    7033,
    7015,
    7018,
    6177,
    6176,
    5781,
    4915,
    1063,
    8893,
    118,
    8460,
    3474,
    8945,
    7945,
    2411,
    519,
    1891,
    6004,
    6012,
    3781,
    1959,
    1912,
    1916,
    2081,
    2036,
    2010,
    3581,
    565,
    529,
    254,
    1434,
    1409,
    1516,
    1183,
    1121,
    1128,
    1224,
    596,
    7399,
    9037,
    7946,
    3991,
    2795,
    6839,
    3809,
    6178,
    6195,
    7981,
    2171,
    6010,
    3782,
    3477,
    1914,
    2378,
    2082,
    2038,
    6013,
    3582,
    567,
    1960,
    1918,
    530,
    1122,
    1195,
    1225,
    597,
    7524,
    2794,
    1410,
    255,
    1517,
    3810,
    7892,
    1439,
    3634,
    1184,
    6266,
    3591,
    8734,
    7525,
    521,
    7749,
    5612,
    314,
    1129,
    2329,
    293,
    4832,
    7696,
    2744,
    2011,
    1303,
    1791,
    1318,
    8810,
    7964,
    4432,
    5246,
    4918,
    1786,
    3035,
    428,
    576,
    3642,
    8811,
    4443,
    4943,
    7967,
    312,
    8005,
    3844,
    8478,
    8891,
    1893,
    4942,
    523,
    7653,
    8479,
    7901,
    7898,
    2139,
    4995,
    140,
    7868,
    7875,
    2142,
    8480,
    141,
    8013,
    7973,
    7970,
    2966,
    8514,
    7988,
    9294,
    373,
    8481,
    3381,
    187,
    1540,
    8486,
    1789,
    4932,
    8284,
    5614,
    1620,
    2827,
    310,
    582,
    8179,
    6043,
    6042,
    7925,
    273,
    7518,
    7915,
    112,
    8012,
    5955,
    8020,
    8306,
    1463,
    1374,
    8181,
    6156,
    7818,
    6045,
    1669,
    6101,
    2172,
    6106,
    6263,
    6242,
    6210,
    6261,
    6207,
    6208,
    7863,
    7996,
    8017,
    6347,
    6345,
    6346,
    8087,
    8091,
    9550,
    8936,
    5220,
    5332,
    1690,
    1820,
    353,
    332,
    315,
    1097,
    1101,
    1102,
    5783,
    2585,
    2143,
    351,
    363,
    336,
    330,
    6744,
    3903,
    8357,
    6742,
    7459,
    3902,
    8753,
    8077,
    8075,
    7974,
    5696,
    6849,
    5331,
    7571,
    8018,
    7397,
    5330,
    8367,
    8512,
    7457,
    7438,
    344,
    4875,
    8086,
    8029,
    8216,
    7698,
    7392,
    5652,
    5380,
    2547,
    354,
    345,
    333,
    318,
    1105,
    8098,
    1881,
    341,
    352,
    365,
    328,
    7700,
    6743,
    8245,
    8217,
    144,
    329,
    375,
    9059,
    343,
    476,
    496,
    1108,
    7729,
    7712,
    5840,
    1696,
    3015,
    1589,
    8269,
    6675,
    6240,
    320,
    313,
    6673,
    1707,
    6674,
    5216,
    5020,
    8482,
    1594,
    1098,
    5259,
    5123,
    1813,
    1599,
    451,
    8484,
    8749,
    8483,
    8122,
    8068,
    8072,
    8053,
    8057,
    9742,
    9526,
    9135,
    9081,
    8803,
    8801,
    8812,
    8799,
    8797,
    8794,
    7721,
    7720,
    7701,
    7647,
    7398,
    4038,
    2032,
    338,
    865,
    839,
    822,
    1611,
    6262,
    1099,
    8485,
    9133,
    8099,
    146,
    8739,
    7727,
    7223,
    8804,
    7723,
    843,
    8183,
    717,
    147,
    1378,
    7703,
    7702,
    7708,
    7707,
    7705,
    7704,
    6241,
    1100,
    493,
    185,
    242,
    8450,
    8415,
    8411,
    8887,
    8857,
    8815,
    9010,
    8934,
    5957,
    6140,
    5784,
    7722,
    7625,
    3749,
    5629,
    2174,
    1977,
    3296,
    3297,
    158,
    1296,
    9548,
    8922,
    1955,
    855,
    9008,
    2162,
    1391,
    608,
    8184,
    9018,
    8294,
    8859,
    8858,
    7725,
    8689,
    7718,
    3302,
    3840,
    3283,
    5626,
    5625,
    1330,
    7522,
    3392,
    3298,
    3299,
    8124,
    8206,
    9087,
    8894,
    8947,
    8916,
    7400,
    5541,
    5482,
    2017,
    2181,
    3829,
    22,
    3849,
    3918,
    5494,
    5890,
    7113,
    7321,
    7348,
    5498,
    24,
    7322,
    3852,
    3919,
    7114,
    4056,
    4058,
    3640
]

print(str(len(list1)) + "-----------" + str(len(set(list1))))
print(str(len(list2)) + "-----------" + str(len(set(list2))))
list3 = list(set(list1).difference(set(list2)))
print(str(len(list3)) + "-----------" + str(len(set(list3))))
for i in list1:
    if i not in list2:
        print(i)


# list4 = [
#
# ]
# print(len(set(list4)))
# for i in set(list4):
#     print(i)