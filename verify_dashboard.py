from app import create_app
from app.routes.dashboard import _aggregate
from datetime import date, timedelta

app = create_app()

with app.app_context():
    start = date.today() - timedelta(days=7)
    end = date.today()
    
    print(f"Testing aggregation from {start} to {end}")
    
    matrix, summary, dates = _aggregate(start, end)
    
    print(f"Dates returned: {len(dates)}")
    for d in dates:
        print(d.strftime('%Y-%m-%d'))
        
    print("\nMatrix Sample:")
    if matrix:
        first_doc = list(matrix.keys())[0]
        print(f"Doctor: {first_doc}")
        for day in dates:
            d_str = day.strftime('%Y-%m-%d')
            cell = matrix[first_doc][d_str]
            if cell:
                print(f"  {d_str}: {dict(cell)}")
    else:
        print("Matrix empty (expected if DB empty or no logs)")

    print("\nSummary Sample:")
    print(dict(summary))
