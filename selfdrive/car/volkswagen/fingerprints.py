from cereal import car
from openpilot.selfdrive.car.volkswagen.values import CAR

Ecu = car.CarParams.Ecu

# TODO: Sharan Mk2 EPS and DQ250 auto trans both require KWP2000 support for fingerprinting


FW_VERSIONS = {
  CAR.VOLKSWAGEN_ARTEON_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x873G0906259AH\xf1\x890001',
      b'\xf1\x873G0906259F \xf1\x890004',
      b'\xf1\x873G0906259G \xf1\x890004',
      b'\xf1\x873G0906259G \xf1\x890005',
      b'\xf1\x873G0906259M \xf1\x890003',
      b'\xf1\x873G0906259N \xf1\x890004',
      b'\xf1\x873G0906259P \xf1\x890001',
      b'\xf1\x875NA907115H \xf1\x890002',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927158L \xf1\x893611',
      b'\xf1\x870DL300014C \xf1\x893704',
      b'\xf1\x870GC300011L \xf1\x891401',
      b'\xf1\x870GC300014M \xf1\x892802',
      b'\xf1\x870GC300019G \xf1\x892804',
      b'\xf1\x870GC300040P \xf1\x891401',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572T \xf1\x890383',
      b'\xf1\x875Q0907572J \xf1\x890654',
      b'\xf1\x875Q0907572R \xf1\x890771',
    ],
  },
  CAR.VOLKSWAGEN_ATLAS_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8703H906026AA\xf1\x899970',
      b'\xf1\x8703H906026AG\xf1\x899973',
      b'\xf1\x8703H906026AJ\xf1\x890638',
      b'\xf1\x8703H906026AJ\xf1\x891017',
      b'\xf1\x8703H906026AT\xf1\x891922',
      b'\xf1\x8703H906026BC\xf1\x892664',
      b'\xf1\x8703H906026F \xf1\x896696',
      b'\xf1\x8703H906026F \xf1\x899970',
      b'\xf1\x8703H906026J \xf1\x896026',
      b'\xf1\x8703H906026J \xf1\x899971',
      b'\xf1\x8703H906026S \xf1\x896693',
      b'\xf1\x8703H906026S \xf1\x899970',
      b'\xf1\x873CN906259  \xf1\x890005',
      b'\xf1\x873CN906259F \xf1\x890002',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927158A \xf1\x893387',
      b'\xf1\x8709G927158DR\xf1\x893536',
      b'\xf1\x8709G927158DR\xf1\x893742',
      b'\xf1\x8709G927158EN\xf1\x893691',
      b'\xf1\x8709G927158F \xf1\x893489',
      b'\xf1\x8709G927158FT\xf1\x893835',
      b'\xf1\x8709G927158GL\xf1\x893939',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572R \xf1\x890372',
      b'\xf1\x872Q0907572T \xf1\x890383',
      b'\xf1\x875Q0907572H \xf1\x890620',
      b'\xf1\x875Q0907572J \xf1\x890654',
      b'\xf1\x875Q0907572P \xf1\x890682',
    ],
  },
  CAR.VOLKSWAGEN_CADDY_MK3: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906027T \xf1\x892363',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x877N0907572C \xf1\x890211\xf1\x82\x0155',
    ],
  },
  CAR.VOLKSWAGEN_CRAFTER_MK2: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704L906056BP\xf1\x894729',
      b'\xf1\x8704L906056EK\xf1\x896391',
      b'\xf1\x8705L906023BC\xf1\x892688',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572J \xf1\x890156',
      b'\xf1\x872Q0907572M \xf1\x890233',
    ],
  },
  CAR.VOLKSWAGEN_GOLF_MK7: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906016A \xf1\x897697',
      b'\xf1\x8704E906016AD\xf1\x895758',
      b'\xf1\x8704E906016CE\xf1\x899096',
      b'\xf1\x8704E906016CH\xf1\x899226',
      b'\xf1\x8704E906016N \xf1\x899105',
      b'\xf1\x8704E906023AG\xf1\x891726',
      b'\xf1\x8704E906023BN\xf1\x894518',
      b'\xf1\x8704E906024K \xf1\x896811',
      b'\xf1\x8704E906024K \xf1\x899970',
      b'\xf1\x8704E906027GR\xf1\x892394',
      b'\xf1\x8704E906027HD\xf1\x892603',
      b'\xf1\x8704E906027HD\xf1\x893742',
      b'\xf1\x8704E906027MA\xf1\x894958',
      b'\xf1\x8704L906021DT\xf1\x895520',
      b'\xf1\x8704L906021DT\xf1\x898127',
      b'\xf1\x8704L906021N \xf1\x895518',
      b'\xf1\x8704L906021N \xf1\x898138',
      b'\xf1\x8704L906026BN\xf1\x891197',
      b'\xf1\x8704L906026BP\xf1\x897608',
      b'\xf1\x8704L906026NF\xf1\x899528',
      b'\xf1\x8704L906056CL\xf1\x893823',
      b'\xf1\x8704L906056CR\xf1\x895813',
      b'\xf1\x8704L906056HE\xf1\x893758',
      b'\xf1\x8704L906056HN\xf1\x896590',
      b'\xf1\x8704L906056HT\xf1\x896591',
      b'\xf1\x870EA906016A \xf1\x898343',
      b'\xf1\x870EA906016E \xf1\x894219',
      b'\xf1\x870EA906016F \xf1\x894238',
      b'\xf1\x870EA906016F \xf1\x895002',
      b'\xf1\x870EA906016Q \xf1\x895993',
      b'\xf1\x870EA906016S \xf1\x897207',
      b'\xf1\x875G0906259  \xf1\x890007',
      b'\xf1\x875G0906259D \xf1\x890002',
      b'\xf1\x875G0906259J \xf1\x890002',
      b'\xf1\x875G0906259L \xf1\x890002',
      b'\xf1\x875G0906259N \xf1\x890003',
      b'\xf1\x875G0906259Q \xf1\x890002',
      b'\xf1\x875G0906259Q \xf1\x892313',
      b'\xf1\x875G0906259T \xf1\x890003',
      b'\xf1\x878V0906259H \xf1\x890002',
      b'\xf1\x878V0906259J \xf1\x890003',
      b'\xf1\x878V0906259J \xf1\x890103',
      b'\xf1\x878V0906259K \xf1\x890001',
      b'\xf1\x878V0906259K \xf1\x890003',
      b'\xf1\x878V0906259P \xf1\x890001',
      b'\xf1\x878V0906259Q \xf1\x890002',
      b'\xf1\x878V0906259R \xf1\x890002',
      b'\xf1\x878V0906264F \xf1\x890003',
      b'\xf1\x878V0906264L \xf1\x890002',
      b'\xf1\x878V0906264M \xf1\x890001',
      b'\xf1\x878V09C0BB01 \xf1\x890001',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927749AP\xf1\x892943',
      b'\xf1\x8709S927158A \xf1\x893585',
      b'\xf1\x870CW300040H \xf1\x890606',
      b'\xf1\x870CW300041D \xf1\x891004',
      b'\xf1\x870CW300041H \xf1\x891010',
      b'\xf1\x870CW300042F \xf1\x891604',
      b'\xf1\x870CW300043B \xf1\x891601',
      b'\xf1\x870CW300043E \xf1\x891603',
      b'\xf1\x870CW300044S \xf1\x894530',
      b'\xf1\x870CW300044T \xf1\x895245',
      b'\xf1\x870CW300045  \xf1\x894531',
      b'\xf1\x870CW300047D \xf1\x895261',
      b'\xf1\x870CW300047E \xf1\x895261',
      b'\xf1\x870CW300048J \xf1\x890611',
      b'\xf1\x870CW300049H \xf1\x890905',
      b'\xf1\x870CW300050G \xf1\x891905',
      b'\xf1\x870D9300012  \xf1\x894904',
      b'\xf1\x870D9300012  \xf1\x894913',
      b'\xf1\x870D9300012  \xf1\x894937',
      b'\xf1\x870D9300012  \xf1\x895045',
      b'\xf1\x870D9300012  \xf1\x895046',
      b'\xf1\x870D9300014M \xf1\x895004',
      b'\xf1\x870D9300014Q \xf1\x895006',
      b'\xf1\x870D9300020J \xf1\x894902',
      b'\xf1\x870D9300020Q \xf1\x895201',
      b'\xf1\x870D9300020S \xf1\x895201',
      b'\xf1\x870D9300040A \xf1\x893613',
      b'\xf1\x870D9300040S \xf1\x894311',
      b'\xf1\x870D9300041H \xf1\x895220',
      b'\xf1\x870D9300041P \xf1\x894507',
      b'\xf1\x870DD300045K \xf1\x891120',
      b'\xf1\x870DD300046F \xf1\x891601',
      b'\xf1\x870GC300012A \xf1\x891401',
      b'\xf1\x870GC300012A \xf1\x891403',
      b'\xf1\x870GC300012M \xf1\x892301',
      b'\xf1\x870GC300014B \xf1\x892401',
      b'\xf1\x870GC300014B \xf1\x892403',
      b'\xf1\x870GC300014B \xf1\x892405',
      b'\xf1\x870GC300020G \xf1\x892401',
      b'\xf1\x870GC300020G \xf1\x892403',
      b'\xf1\x870GC300020G \xf1\x892404',
      b'\xf1\x870GC300020N \xf1\x892804',
      b'\xf1\x870GC300043T \xf1\x899999',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x875Q0907567G \xf1\x890390\xf1\x82\x0101',
      b'\xf1\x875Q0907567J \xf1\x890396\xf1\x82\x0101',
      b'\xf1\x875Q0907567L \xf1\x890098\xf1\x82\x0101',
      b'\xf1\x875Q0907572A \xf1\x890141\xf1\x82\x0101',
      b'\xf1\x875Q0907572B \xf1\x890200\xf1\x82\x0101',
      b'\xf1\x875Q0907572C \xf1\x890210\xf1\x82\x0101',
      b'\xf1\x875Q0907572D \xf1\x890304\xf1\x82\x0101',
      b'\xf1\x875Q0907572E \xf1\x89X310\xf1\x82\x0101',
      b'\xf1\x875Q0907572F \xf1\x890400\xf1\x82\x0101',
      b'\xf1\x875Q0907572G \xf1\x890571',
      b'\xf1\x875Q0907572H \xf1\x890620',
      b'\xf1\x875Q0907572J \xf1\x890653',
      b'\xf1\x875Q0907572J \xf1\x890654',
      b'\xf1\x875Q0907572P \xf1\x890682',
      b'\xf1\x875Q0907572R \xf1\x890771',
      b'\xf1\x875Q0907572S \xf1\x890780',
    ],
  },
  CAR.VOLKSWAGEN_JETTA_MK7: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906024AK\xf1\x899937',
      b'\xf1\x8704E906024AS\xf1\x899912',
      b'\xf1\x8704E906024B \xf1\x895594',
      b'\xf1\x8704E906024BC\xf1\x899971',
      b'\xf1\x8704E906024BG\xf1\x891057',
      b'\xf1\x8704E906024C \xf1\x899970',
      b'\xf1\x8704E906024C \xf1\x899971',
      b'\xf1\x8704E906024L \xf1\x895595',
      b'\xf1\x8704E906024L \xf1\x899970',
      b'\xf1\x8704E906027MS\xf1\x896223',
      b'\xf1\x8705E906013DB\xf1\x893361',
      b'\xf1\x875G0906259T \xf1\x890003',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927158BQ\xf1\x893545',
      b'\xf1\x8709S927158BS\xf1\x893642',
      b'\xf1\x8709S927158BS\xf1\x893694',
      b'\xf1\x8709S927158CK\xf1\x893770',
      b'\xf1\x8709S927158JC\xf1\x894113',
      b'\xf1\x8709S927158R \xf1\x893552',
      b'\xf1\x8709S927158R \xf1\x893587',
      b'\xf1\x870GC300020N \xf1\x892803',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x875Q0907572N \xf1\x890681',
      b'\xf1\x875Q0907572P \xf1\x890682',
      b'\xf1\x875Q0907572R \xf1\x890771',
    ],
  },
  CAR.VOLKSWAGEN_PASSAT_MK8: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8703N906026E \xf1\x892114',
      b'\xf1\x8704E906023AH\xf1\x893379',
      b'\xf1\x8704E906023BM\xf1\x894522',
      b'\xf1\x8704L906026DP\xf1\x891538',
      b'\xf1\x8704L906026ET\xf1\x891990',
      b'\xf1\x8704L906026FP\xf1\x892012',
      b'\xf1\x8704L906026GA\xf1\x892013',
      b'\xf1\x8704L906026GK\xf1\x899971',
      b'\xf1\x8704L906026KD\xf1\x894798',
      b'\xf1\x8705L906022A \xf1\x890827',
      b'\xf1\x873G0906259  \xf1\x890004',
      b'\xf1\x873G0906259B \xf1\x890002',
      b'\xf1\x873G0906264  \xf1\x890004',
      b'\xf1\x8704E906027BS\xf1\x892887',
      b'\xf1\x8704E906027BT\xf1\x899042',
      b'\xf1\x8704L906026ET\xf1\x891343',
      b'\xf1\x8704L906026ET\xf1\x891990',
      b'\xf1\x8704L906026FP\xf1\x891196',
      b'\xf1\x8704L906026KA\xf1\x896014',
      b'\xf1\x8704L906026KB\xf1\x894071',
      b'\xf1\x8704L906026KD\xf1\x894798',
      b'\xf1\x8704L906026MT\xf1\x893076',
      b'\xf1\x8705L906022BK\xf1\x899971',
      b'\xf1\x873G0906259  \xf1\x890004',
      b'\xf1\x873G0906259B \xf1\x890002',
      b'\xf1\x873G0906259L \xf1\x890003',
      b'\xf1\x873G0906264A \xf1\x890002',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300041E \xf1\x891006',
      b'\xf1\x870CW300042H \xf1\x891601',
      b'\xf1\x870CW300042H \xf1\x891607',
      b'\xf1\x870CW300043H \xf1\x891601',
      b'\xf1\x870CW300048R \xf1\x890610',
      b'\xf1\x870D9300013A \xf1\x894905',
      b'\xf1\x870D9300014L \xf1\x895002',
      b'\xf1\x870D9300018C \xf1\x895297',
      b'\xf1\x870D9300041A \xf1\x894801',
      b'\xf1\x870D9300042H \xf1\x894901',
      b'\xf1\x870DD300045T \xf1\x891601',
      b'\xf1\x870DD300046H \xf1\x891601',
      b'\xf1\x870DL300011H \xf1\x895201',
      b'\xf1\x870GC300042H \xf1\x891404',
      b'\xf1\x870GC300043  \xf1\x892301',
      b'\xf1\x870GC300046P \xf1\x892805',
      b'\xf1\x870CW300042H \xf1\x891601',
      b'\xf1\x870CW300043B \xf1\x891603',
      b'\xf1\x870CW300049Q \xf1\x890906',
      b'\xf1\x870D9300011T \xf1\x894801',
      b'\xf1\x870D9300012  \xf1\x894940',
      b'\xf1\x870D9300013A \xf1\x894905',
      b'\xf1\x870D9300014K \xf1\x895006',
      b'\xf1\x870D9300041H \xf1\x894905',
      b'\xf1\x870D9300042M \xf1\x895013',
      b'\xf1\x870D9300043F \xf1\x895202',
      b'\xf1\x870GC300013K \xf1\x892403',
      b'\xf1\x870GC300014M \xf1\x892801',
      b'\xf1\x870GC300019G \xf1\x892803',
      b'\xf1\x870GC300043  \xf1\x892301',
      b'\xf1\x870GC300046D \xf1\x892402',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x873Q0907572A \xf1\x890126',
      b'\xf1\x873Q0907572A \xf1\x890130',
      b'\xf1\x873Q0907572B \xf1\x890192',
      b'\xf1\x873Q0907572B \xf1\x890194',
      b'\xf1\x873Q0907572C \xf1\x890195',
      b'\xf1\x873Q0907572C \xf1\x890196',
      b'\xf1\x875Q0907572P \xf1\x890682',
      b'\xf1\x875Q0907572R \xf1\x890771',
      b'\xf1\x873Q0907572B \xf1\x890192',
      b'\xf1\x873Q0907572B \xf1\x890194',
      b'\xf1\x873Q0907572C \xf1\x890195',
      b'\xf1\x875Q0907572R \xf1\x890771',
      b'\xf1\x875Q0907572S \xf1\x890780',
    ],
  },
  CAR.VOLKSWAGEN_PASSAT_NMS: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8706K906016C \xf1\x899609',
      b'\xf1\x8706K906016E \xf1\x899830',
      b'\xf1\x8706K906016G \xf1\x891124',
      b'\xf1\x8706K906071BJ\xf1\x894891',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927158AB\xf1\x893318',
      b'\xf1\x8709G927158BD\xf1\x893121',
      b'\xf1\x8709G927158DK\xf1\x893594',
      b'\xf1\x8709G927158FQ\xf1\x893745',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x87561907567A \xf1\x890132',
      b'\xf1\x877N0907572C \xf1\x890211\xf1\x82\x0152',
    ],
  },
  CAR.VOLKSWAGEN_POLO_MK6: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704C906025H \xf1\x895177',
      b'\xf1\x8705C906032J \xf1\x891702',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300042D \xf1\x891612',
      b'\xf1\x870CW300050D \xf1\x891908',
      b'\xf1\x870CW300051G \xf1\x891909',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572R \xf1\x890372',
    ],
  },
  CAR.VOLKSWAGEN_SHARAN_MK2: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704L906016HE\xf1\x894635',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x877N0907572C \xf1\x890211\xf1\x82\x0153',
    ],
  },
  CAR.VOLKSWAGEN_TAOS_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906025CK\xf1\x892228',
      b'\xf1\x8704E906027NJ\xf1\x891445',
      b'\xf1\x8704E906027NP\xf1\x891286',
      b'\xf1\x8705E906013BD\xf1\x892496',
      b'\xf1\x8705E906013E \xf1\x891624',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927158EM\xf1\x893812',
      b'\xf1\x8709S927158BL\xf1\x893791',
      b'\xf1\x8709S927158CR\xf1\x893924',
      b'\xf1\x8709S927158DN\xf1\x893946',
      b'\xf1\x8709S927158FF\xf1\x893876',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.VOLKSWAGEN_TCROSS_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704C906025AK\xf1\x897053',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300050E \xf1\x891903',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.VOLKSWAGEN_TIGUAN_MK2: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8703N906026D \xf1\x893680',
      b'\xf1\x8704E906024AP\xf1\x891461',
      b'\xf1\x8704E906027NB\xf1\x899504',
      b'\xf1\x8704L906026EJ\xf1\x893661',
      b'\xf1\x8704L906027G \xf1\x899893',
      b'\xf1\x8705E906018BS\xf1\x890914',
      b'\xf1\x875N0906259  \xf1\x890002',
      b'\xf1\x875NA906259H \xf1\x890002',
      b'\xf1\x875NA907115E \xf1\x890003',
      b'\xf1\x875NA907115E \xf1\x890005',
      b'\xf1\x875NA907115J \xf1\x890002',
      b'\xf1\x875NA907115K \xf1\x890004',
      b'\xf1\x8783A907115  \xf1\x890007',
      b'\xf1\x8783A907115B \xf1\x890005',
      b'\xf1\x8783A907115F \xf1\x890002',
      b'\xf1\x8783A907115G \xf1\x890001',
      b'\xf1\x8783A907115K \xf1\x890001',
      b'\xf1\x8783A907115K \xf1\x890002',
      b'\xf1\x8783A907115Q \xf1\x890001',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927158DT\xf1\x893698',
      b'\xf1\x8709G927158FM\xf1\x893757',
      b'\xf1\x8709G927158GC\xf1\x893821',
      b'\xf1\x8709G927158GD\xf1\x893820',
      b'\xf1\x8709G927158GM\xf1\x893936',
      b'\xf1\x8709G927158GN\xf1\x893938',
      b'\xf1\x8709G927158HB\xf1\x894069',
      b'\xf1\x8709G927158HC\xf1\x894070',
      b'\xf1\x870D9300043  \xf1\x895202',
      b'\xf1\x870DD300046K \xf1\x892302',
      b'\xf1\x870DL300011N \xf1\x892001',
      b'\xf1\x870DL300011N \xf1\x892012',
      b'\xf1\x870DL300012M \xf1\x892107',
      b'\xf1\x870DL300012P \xf1\x892103',
      b'\xf1\x870DL300013A \xf1\x893005',
      b'\xf1\x870DL300013G \xf1\x892119',
      b'\xf1\x870DL300013G \xf1\x892120',
      b'\xf1\x870DL300014C \xf1\x893703',
      b'\xf1\x870GC300013P \xf1\x892401',
      b'\xf1\x870GC300046Q \xf1\x892802',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572AB\xf1\x890397',
      b'\xf1\x872Q0907572J \xf1\x890156',
      b'\xf1\x872Q0907572M \xf1\x890233',
      b'\xf1\x872Q0907572Q \xf1\x890342',
      b'\xf1\x872Q0907572R \xf1\x890372',
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.VOLKSWAGEN_TOURAN_MK2: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906025BE\xf1\x890720',
      b'\xf1\x8704E906027HQ\xf1\x893746',
      b'\xf1\x8704L906026HM\xf1\x893017',
      b'\xf1\x8705E906018CQ\xf1\x890808',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300020A \xf1\x891936',
      b'\xf1\x870CW300041E \xf1\x891005',
      b'\xf1\x870CW300041Q \xf1\x891606',
      b'\xf1\x870CW300051M \xf1\x891926',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x873Q0907572C \xf1\x890195',
      b'\xf1\x875Q0907572R \xf1\x890771',
    ],
  },
  CAR.VOLKSWAGEN_TRANSPORTER_T61: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704L906056AG\xf1\x899970',
      b'\xf1\x8704L906056AL\xf1\x899970',
      b'\xf1\x8704L906057AP\xf1\x891186',
      b'\xf1\x8704L906057N \xf1\x890413',
      b'\xf1\x8705L906023E \xf1\x891352',
      b'\xf1\x8705L906023MR\xf1\x892582',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870BT300012E \xf1\x893105',
      b'\xf1\x870BT300012G \xf1\x893102',
      b'\xf1\x870BT300046R \xf1\x893102',
      b'\xf1\x870DV300012B \xf1\x893701',
      b'\xf1\x870DV300012B \xf1\x893702',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572R \xf1\x890372',
    ],
  },
  CAR.VOLKSWAGEN_TROC_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8705E906018AT\xf1\x899640',
      b'\xf1\x8705E906018CK\xf1\x890863',
      b'\xf1\x8705E906018P \xf1\x896020',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300041S \xf1\x891615',
      b'\xf1\x870CW300050J \xf1\x891911',
      b'\xf1\x870CW300051M \xf1\x891925',
      b'\xf1\x870CW300051M \xf1\x891928',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572M \xf1\x890233',
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.AUDI_A3_MK3: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906023AN\xf1\x893695',
      b'\xf1\x8704E906023AR\xf1\x893440',
      b'\xf1\x8704E906023BL\xf1\x895190',
      b'\xf1\x8704E906027CJ\xf1\x897798',
      b'\xf1\x8704L997022N \xf1\x899459',
      b'\xf1\x875G0906259A \xf1\x890004',
      b'\xf1\x875G0906259D \xf1\x890002',
      b'\xf1\x875G0906259L \xf1\x890002',
      b'\xf1\x875G0906259Q \xf1\x890002',
      b'\xf1\x878V0906259E \xf1\x890001',
      b'\xf1\x878V0906259F \xf1\x890002',
      b'\xf1\x878V0906259H \xf1\x890002',
      b'\xf1\x878V0906259J \xf1\x890002',
      b'\xf1\x878V0906259K \xf1\x890001',
      b'\xf1\x878V0906264B \xf1\x890003',
      b'\xf1\x878V0907115B \xf1\x890007',
      b'\xf1\x878V0907404A \xf1\x890005',
      b'\xf1\x878V0907404G \xf1\x890005',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300044T \xf1\x895245',
      b'\xf1\x870CW300048  \xf1\x895201',
      b'\xf1\x870D9300012  \xf1\x894912',
      b'\xf1\x870D9300012  \xf1\x894931',
      b'\xf1\x870D9300012K \xf1\x894513',
      b'\xf1\x870D9300012L \xf1\x894521',
      b'\xf1\x870D9300013B \xf1\x894902',
      b'\xf1\x870D9300013B \xf1\x894931',
      b'\xf1\x870D9300041N \xf1\x894512',
      b'\xf1\x870D9300043T \xf1\x899699',
      b'\xf1\x870DD300046  \xf1\x891604',
      b'\xf1\x870DD300046A \xf1\x891602',
      b'\xf1\x870DD300046F \xf1\x891602',
      b'\xf1\x870DD300046G \xf1\x891601',
      b'\xf1\x870DL300012E \xf1\x892012',
      b'\xf1\x870DL300012H \xf1\x892112',
      b'\xf1\x870GC300011  \xf1\x890403',
      b'\xf1\x870GC300013M \xf1\x892402',
      b'\xf1\x870GC300042J \xf1\x891402',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x875Q0907567M \xf1\x890398\xf1\x82\x0101',
      b'\xf1\x875Q0907567N \xf1\x890400\xf1\x82\x0101',
      b'\xf1\x875Q0907572D \xf1\x890304\xf1\x82\x0101',
      b'\xf1\x875Q0907572F \xf1\x890400\xf1\x82\x0101',
      b'\xf1\x875Q0907572G \xf1\x890571',
      b'\xf1\x875Q0907572H \xf1\x890620',
      b'\xf1\x875Q0907572P \xf1\x890682',
    ],
  },
  CAR.AUDI_Q2_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906027JT\xf1\x894145',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300041F \xf1\x891006',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572M \xf1\x890233',
    ],
  },
  CAR.AUDI_Q3_MK2: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8705E906018N \xf1\x899970',
      b'\xf1\x8705L906022M \xf1\x890901',
      b'\xf1\x8783A906259  \xf1\x890001',
      b'\xf1\x8783A906259  \xf1\x890005',
      b'\xf1\x8783A906259C \xf1\x890002',
      b'\xf1\x8783A906259D \xf1\x890001',
      b'\xf1\x8783A906259F \xf1\x890001',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x8709G927158CN\xf1\x893608',
      b'\xf1\x8709G927158FL\xf1\x893758',
      b'\xf1\x8709G927158GG\xf1\x893825',
      b'\xf1\x8709G927158GP\xf1\x893937',
      b'\xf1\x870GC300045D \xf1\x892802',
      b'\xf1\x870GC300046F \xf1\x892701',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572R \xf1\x890372',
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.SEAT_ATECA_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906027KA\xf1\x893749',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870D9300014S \xf1\x895202',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572M \xf1\x890233',
    ],
  },
  CAR.SEAT_LEON_MK3: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704L906021EL\xf1\x897542',
      b'\xf1\x8704L906026BP\xf1\x891198',
      b'\xf1\x8704L906026BP\xf1\x897608',
      b'\xf1\x8704L906056CR\xf1\x892181',
      b'\xf1\x8704L906056CR\xf1\x892797',
      b'\xf1\x8705E906018AS\xf1\x899596',
      b'\xf1\x878V0906264H \xf1\x890005',
      b'\xf1\x878V0907115E \xf1\x890002',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300041D \xf1\x891004',
      b'\xf1\x870CW300041G \xf1\x891003',
      b'\xf1\x870CW300050J \xf1\x891908',
      b'\xf1\x870D9300042M \xf1\x895016',
      b'\xf1\x870GC300043A \xf1\x892304',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x875Q0907572B \xf1\x890200\xf1\x82\x0101',
      b'\xf1\x875Q0907572H \xf1\x890620',
      b'\xf1\x875Q0907572K \xf1\x890402\xf1\x82\x0101',
      b'\xf1\x875Q0907572P \xf1\x890682',
      b'\xf1\x875Q0907572R \xf1\x890771',
    ],
  },
  CAR.SKODA_FABIA_MK4: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8705E906018CF\xf1\x891905',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300051M \xf1\x891936',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
    ],
  },
  CAR.SKODA_KAMIQ_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8705C906032M \xf1\x891333',
      b'\xf1\x8705E906013CK\xf1\x892540',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300020  \xf1\x891906',
      b'\xf1\x870CW300020T \xf1\x892204',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.SKODA_KAROQ_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8705E906013CL\xf1\x892541',
      b'\xf1\x8705E906013H \xf1\x892407',
      b'\xf1\x8705E906018P \xf1\x895472',
      b'\xf1\x8705E906018P \xf1\x896020',
      b'\xf1\x8705L906022BS\xf1\x890913',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300020T \xf1\x892202',
      b'\xf1\x870CW300041S \xf1\x891615',
      b'\xf1\x870GC300014L \xf1\x892802',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572AB\xf1\x890397',
      b'\xf1\x872Q0907572M \xf1\x890233',
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.SKODA_KODIAQ_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704E906027DD\xf1\x893123',
      b'\xf1\x8704E906027LD\xf1\x893433',
      b'\xf1\x8704E906027NB\xf1\x896517',
      b'\xf1\x8704E906027NB\xf1\x899504',
      b'\xf1\x8704L906026DE\xf1\x895418',
      b'\xf1\x8704L906026EJ\xf1\x893661',
      b'\xf1\x8704L906026HT\xf1\x893617',
      b'\xf1\x8705E906018DJ\xf1\x890915',
      b'\xf1\x8705E906018DJ\xf1\x891903',
      b'\xf1\x8705L906022GM\xf1\x893411',
      b'\xf1\x875NA906259E \xf1\x890003',
      b'\xf1\x875NA907115D \xf1\x890003',
      b'\xf1\x875NA907115E \xf1\x890003',
      b'\xf1\x875NA907115E \xf1\x890005',
      b'\xf1\x8783A907115E \xf1\x890001',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870D9300014S \xf1\x895201',
      b'\xf1\x870D9300043  \xf1\x895202',
      b'\xf1\x870DL300011N \xf1\x892014',
      b'\xf1\x870DL300012G \xf1\x892006',
      b'\xf1\x870DL300012M \xf1\x892107',
      b'\xf1\x870DL300012N \xf1\x892110',
      b'\xf1\x870DL300013G \xf1\x892119',
      b'\xf1\x870GC300014N \xf1\x892801',
      b'\xf1\x870GC300018S \xf1\x892803',
      b'\xf1\x870GC300019H \xf1\x892806',
      b'\xf1\x870GC300046Q \xf1\x892802',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572AB\xf1\x890397',
      b'\xf1\x872Q0907572M \xf1\x890233',
      b'\xf1\x872Q0907572Q \xf1\x890342',
      b'\xf1\x872Q0907572R \xf1\x890372',
      b'\xf1\x872Q0907572T \xf1\x890383',
    ],
  },
  CAR.SKODA_OCTAVIA_MK3: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704C906025L \xf1\x896198',
      b'\xf1\x8704E906016ER\xf1\x895823',
      b'\xf1\x8704E906027HD\xf1\x893742',
      b'\xf1\x8704E906027MH\xf1\x894786',
      b'\xf1\x8704L906021DT\xf1\x898127',
      b'\xf1\x8704L906021ER\xf1\x898361',
      b'\xf1\x8704L906026BP\xf1\x897608',
      b'\xf1\x8704L906026BS\xf1\x891541',
      b'\xf1\x8704L906026BT\xf1\x897612',
      b'\xf1\x875G0906259C \xf1\x890002',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300041L \xf1\x891601',
      b'\xf1\x870CW300041N \xf1\x891605',
      b'\xf1\x870CW300043B \xf1\x891601',
      b'\xf1\x870CW300043P \xf1\x891605',
      b'\xf1\x870D9300012H \xf1\x894518',
      b'\xf1\x870D9300014T \xf1\x895221',
      b'\xf1\x870D9300041C \xf1\x894936',
      b'\xf1\x870D9300041H \xf1\x895220',
      b'\xf1\x870D9300041J \xf1\x894902',
      b'\xf1\x870D9300041P \xf1\x894507',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x875Q0907567P \xf1\x890100\xf1\x82\x0101',
      b'\xf1\x875Q0907572D \xf1\x890304\xf1\x82\x0101',
      b'\xf1\x875Q0907572F \xf1\x890400\xf1\x82\x0101',
      b'\xf1\x875Q0907572H \xf1\x890620',
      b'\xf1\x875Q0907572J \xf1\x890654',
      b'\xf1\x875Q0907572K \xf1\x890402\xf1\x82\x0101',
      b'\xf1\x875Q0907572P \xf1\x890682',
      b'\xf1\x875Q0907572R \xf1\x890771',
    ],
  },
  CAR.SKODA_SCALA_MK1: {
    (Ecu.engine, 0x7e0, None): [
      b'\xf1\x8704C906025AK\xf1\x897053',
      b'\xf1\x8705C906032M \xf1\x892365',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'\xf1\x870CW300020  \xf1\x891907',
      b'\xf1\x870CW300050  \xf1\x891709',
    ],
    (Ecu.fwdRadar, 0x757, None): [
      b'\xf1\x872Q0907572AA\xf1\x890396',
      b'\xf1\x872Q0907572R \xf1\x890372',
    ],
  },
}
