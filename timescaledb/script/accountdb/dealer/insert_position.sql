
delete from dealer.positions where tdate >= '2023-06-30';
select * from dealer.positions where tdate = '2023-07-07';

--06-30
CALL dealer.sp_insert_position_tmp('2023-06-30',  6, '8324',  5,  55.3, -1.25, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-06-30', 16, '3563',  1, 232.0, -0.85, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-06-30',  6, '3563',  2, 232.0,  2.65, '2023-06-27');
CALL dealer.sp_insert_position_tmp('2023-06-30',  2, '1513',  1, 137.0,  2.62, '2023-06-26');
CALL dealer.sp_insert_position_tmp('2023-06-30', 16, '8996',  1, 338.5,  4.48, '2023-06-26');
CALL dealer.sp_insert_position_tmp('2023-06-30', 18, '1108',  3,  17.0,  5.37, '2023-06-12');

--07-03
CALL dealer.sp_insert_position_tmp('2023-07-03', 19, '2603',  2, 102.5,  3.74, '2023-07-03');
CALL dealer.sp_insert_position_tmp('2023-07-03',  6, '8324',  5,  55.8, -0.36, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-07-03', 16, '3563',  1, 234.5,  0.21, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-07-03',  6, '3563',  2, 234.5,  3.76, '2023-06-27');
CALL dealer.sp_insert_position_tmp('2023-07-03',  2, '1513',  1, 138.0,  3.37, '2023-06-26');
CALL dealer.sp_insert_position_tmp('2023-07-03', 18, '1108',  3, 17.05,  5.68, '2023-06-12');

--07-04
CALL dealer.sp_insert_position_tmp('2023-07-04',  3, '1519',  2, 149.0, -0.67, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-04',  6, '6187',  6, 100.0,  6.27, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-04', 16, '2399', 12, 26.55, -5.18, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-04', 19, '2603',  2, 105.5,  6.78, '2023-07-03');
CALL dealer.sp_insert_position_tmp('2023-07-04',  6, '8324',  5,  55.0, -1.79, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-07-04', 16, '3563',  1, 247.0,  5.56, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-07-04',  2, '1513',  1, 134.5,  0.75, '2023-06-26');
CALL dealer.sp_insert_position_tmp('2023-07-04', 18, '1108',  3,  16.7,  3.51, '2023-06-12');

--07-05
CALL dealer.sp_insert_position_tmp('2023-07-05',  6, '1533',  8,  68.8, -1.71, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-05',  6, '2329', 22, 27.55,  3.57, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-05',  6, '2480',  4, 121.5,  2.10, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-05',  6, '2485', 28, 22.15,  5.48, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-05',  8, '1477',  1, 306.5, -2.39, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-05', 10, '2399', 27, 25.35, -4.08, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-05',  3, '1519',  2, 146.0, -2.67, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-05',  6, '6187',  6, 100.0,  6.27, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-05', 16, '2399', 12, 25.35, -9.46, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-05', 19, '2603',  2, 107.0,  8.30, '2023-07-03');
CALL dealer.sp_insert_position_tmp('2023-07-05', 16, '3563',  1, 243.5,  4.06, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-07-05',  2, '1513',  1, 130.5, -2.25, '2023-06-26');
CALL dealer.sp_insert_position_tmp('2023-07-05', 18, '1108',  3, 16.65,  3.20, '2023-06-12');

--07-06
CALL dealer.sp_insert_position_tmp('2023-07-06', 12, '4968',  6, 186.0,  3.33, '2023-07-06');
CALL dealer.sp_insert_position_tmp('2023-07-06', 15, '3704', 29,  55.7,  1.36, '2023-07-06');
CALL dealer.sp_insert_position_tmp('2023-07-06', 18, '2809',  1, 36.15, -0.14, '2023-07-06');
CALL dealer.sp_insert_position_tmp('2023-07-06',  6, '1533',  8,  67.7, -3.29, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-06',  6, '2329', 22,  27.5,  3.38, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-06',  6, '2480',  4, 120.5,  1.26, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-06',  6, '2485', 28, 21.85,  4.05, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-06',  8, '1477',  1, 303.0, -3.50, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-06',  3, '1519',  2, 149.5, -0.33, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-06',  6, '6187',  6, 110.0, 16.90, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-06', 16, '2399', 12, 25.35, -9.46, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-06', 19, '2603',  2, 106.5,  7.79, '2023-07-03');
CALL dealer.sp_insert_position_tmp('2023-07-06', 16, '3563',  1, 235.5,  0.64, '2023-06-30');
CALL dealer.sp_insert_position_tmp('2023-07-06', 18, '1108',  3,  16.3,  1.03, '2023-06-12');


--07-07
CALL dealer.sp_insert_position_tmp('2023-07-07', 15, '3704', 29,  54.1, -1.55, '2023-07-06');
CALL dealer.sp_insert_position_tmp('2023-07-07', 18, '2809',  1,  36.1, -0.28, '2023-07-06');
CALL dealer.sp_insert_position_tmp('2023-07-07',  6, '1533',  8,  68.1, -2.71, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-07',  6, '2329', 22,  26.6,  0.00, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-07',  6, '2480',  4, 121.5,  2.10, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-07',  6, '2485', 28,  20.7, -1.43, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-07',  8, '1477',  1, 301.0, -4.14, '2023-07-05');
CALL dealer.sp_insert_position_tmp('2023-07-07',  3, '1519',  2, 149.5, -0.33, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-07',  6, '6187',  6, 109.0, 15.83, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-07', 16, '2399', 12,  24.9, -11.07, '2023-07-04');
CALL dealer.sp_insert_position_tmp('2023-07-07', 19, '2603',  2, 108.0,  9.31, '2023-07-03');
