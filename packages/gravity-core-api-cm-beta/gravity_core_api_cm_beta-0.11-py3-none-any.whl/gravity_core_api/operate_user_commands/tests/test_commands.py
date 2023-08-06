from gravity_core_api.tests.test_ar import TestAR


test_ar = TestAR()

all_test_commands = {'get_status':
                         {'test_command':
                              {'user_command': {'get_status': {}}}
                          },
                     'start_car_protocol': {'test_command':
                                               {'user_command': {'start_car_protocol': {'carnum': 'В333ХХ102',
                                                                                        'comm': 'TESTING API',
                                                                                        'course': 'IN',
                                                                                        'car_choose_mode': 'manual',
                                                                                        'dlinnomer': False,
                                                                                        'polomka': False,
                                                                                        'orup_mode': 'orup_extended',
                                                                                        'operator': 'Гульнара',
                                                                                        'carrier': 'test_carrier_1',
                                                                                        'trash_cat': 'ТКО-4',
                                                                                        'trash_type': 'ПО',
                                                                                        'polygon_object': 'Test1',
                                                                                        'carnum_was': None}}}},
                     'operate_gate_manual_control': {'test_command':
                                                         {'user_command': {'operate_gate_manual_control': {'operation': 'close',
                                                                                                           'gate_name': 'entry'}}}}
                     }