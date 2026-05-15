import sys
import json

from zona_calidad_aire.zona_calidad_aire import ZonaCalidadAire
from corredor_emision.corredor_emision import CorredorEmision
from estacion_monitoreo.estacion_monitoreo import EstacionMonitoreo


def get_table_instance(table_name):
    if table_name == "zona_calidad_aire":
        return ZonaCalidadAire()

    if table_name == "corredor_emision":
        return CorredorEmision()

    if table_name == "estacion_monitoreo":
        return EstacionMonitoreo()

    raise Exception(
        "Invalid table name. Use: zona_calidad_aire, corredor_emision or estacion_monitoreo"
    )


def execute_function(table_instance, function_name, data):
    if function_name == "insert":
        return table_instance.insert(data)

    if function_name == "selectAsDicts":
        return table_instance.selectAsDicts(data)

    if function_name == "selectAsTuples":
        return table_instance.selectAsTuples(data)

    if function_name == "selectAllAsDicts":
        return table_instance.selectAllAsDicts()

    if function_name == "update":
        return table_instance.update(data)

    if function_name == "delete":
        return table_instance.delete(data)

    raise Exception(
        "Invalid function name. Use: insert, selectAsDicts, selectAsTuples, selectAllAsDicts, update or delete"
    )


def main():
    if len(sys.argv) < 3:
        print(
            "Use: python main.py table_name function_name '{\"id\":1}'"
        )
        sys.exit(0)

    table_name = sys.argv[1]
    function_name = sys.argv[2]

    if len(sys.argv) >= 4:
        data = json.loads(sys.argv[3])
    else:
        data = {}

    try:
        table_instance = get_table_instance(table_name)
        result = execute_function(table_instance, function_name, data)
        print(result)

    except Exception as e:
        print({
            "ok": False,
            "message": str(e),
            "data": []
        })


if __name__ == "__main__":
    main()