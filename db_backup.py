
import pandas as pd
import db_functions as dbfnc
import config as cfg

my_table_list =[
    'AccessLvlTable', 'AccountingCodeTable','AdvancerTable',
    'CPOCrewingBurnsTable', 'CrewBailoutCounterTable', 'CrewBailoutTypeTable',
    'CrewNamesTable', 'CrewProficiencyTable', 'CrewShiftTypeTable',
    'CrewShiftWorkedTable', 'CrewStatusTable', 'CRFcodes',
    'HeadNamesTable', 'HeadShiftWorkedTable', 'InventoryTable',
    'InventoryUseTable', 'PrefferedAVTable', 'PresenterTable',
    'ProjectorTable ', 'PurchaseOrderTable', 'ScreenSetupTable',
    'ShowStyleTable', 'ShowTable', '[tbl-11-12_dbdata]',
    '[tbl-12-13_dbdata]', '[Tbl-BudgetingCategory]', 'tblConductorGigs',
    'tblConductorNames', 'tblCrewCRFWork', 'tblHeadCRFwork',
    'tblSndMaintShifts', 'tblSndMaintShiftTypes', '[Tbl-TOILpayout]',
    'TMPtblWeeklyCrewData', 'TMPtblWeeklyHeadsData', 'UserTable',
    'VenderTable', 'VenueTable'
    ]

for i in my_table_list:
    query = (f'SELECT * FROM {i}')

    with dbfnc.connection(cfg.my_driver, cfg.my_server, cfg.my_db) as conn:
        df = pd.read_sql(query, conn)
    
    print(i)
    print(df.head(5))
    print()
    
    df.to_csv(f'{cfg.desktop_dir}/{i}.csv')

