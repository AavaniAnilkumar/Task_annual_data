from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
import pandas as pd 
from .models import WellData
# Create your views here.

def download_quarterly_data(request):
    file_url = "https://ohiodnr.gov/static/documents/oil-gas/production/20210309_2020_1%20-%204.xls"
    response = requests.get(file_url)

    if response.status_code == 200:
        response = HttpResponse(response.content, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="20210309_2020_1-4.xls"'
        return response

    return HttpResponse("Failed to download the file.")



def calculate_annual_data(request):
    file_url = "https://ohiodnr.gov/static/documents/oil-gas/production/20210309_2020_1%20-%204.xls"
    response = requests.get(file_url)

    if response.status_code == 200:
        # Save the downloaded file temporarily
        with open("production_data.xls", "wb") as file:
            file.write(response.content)

        # Read the Excel file into a Pandas DataFrame
        data_frame = pd.read_excel("production_data.xls")

        # Calculate the annual data for each well based on API WELL NUMBER
        wells_data = {}
        for index, row in data_frame.iterrows():
            api_well_number = row["API WELL  NUMBER"]
            oil_production = row["OIL"]
            gas_production = row["GAS"]
            brine_production = row["BRINE"]

            if api_well_number not in wells_data:
                wells_data[api_well_number] = {
                    "oil": oil_production,
                    "gas": gas_production,
                    "brine": brine_production
                }
            else:
                wells_data[api_well_number]["oil"] += oil_production
                wells_data[api_well_number]["gas"] += gas_production
                wells_data[api_well_number]["brine"] += brine_production

        

        # Prepare the calculated data as a CSV file
        csv_data = "API WELL NUMBER,OIL,GAS,BRINE\n"
        for api_well_number, production_data in wells_data.items():
            oil_production = production_data["oil"]
            gas_production = production_data["gas"]
            brine_production = production_data["brine"]
            csv_data += f"{api_well_number},{oil_production},{gas_production},{brine_production}\n"

        for api_well_number, production_data in wells_data.items():
            oil_production = production_data["oil"]
            gas_production = production_data["gas"]
            brine_production = production_data["brine"]
            WellData.objects.create(
                api_well_number=api_well_number,
                oil_production=oil_production,
                gas_production=gas_production,
                brine_production=brine_production
            )

        return HttpResponse("Annual data loaded into the database.")

    return HttpResponse("Failed to download the file.")




def get_annual_data(request):
    api_well_number = request.GET.get('well', '')

    try:
        well_data = WellData.objects.get(api_well_number=api_well_number)
        response_data = {
            'oil': well_data.oil_production,
            'gas': well_data.gas_production,
            'brine': well_data.brine_production
        }
        return JsonResponse(response_data)
    except WellData.DoesNotExist:
        return JsonResponse({'error': 'Well data not found'}, status=404)