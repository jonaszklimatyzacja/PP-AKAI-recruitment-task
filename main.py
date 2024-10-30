# Z podanego zbioru danych wyselekcjonuj 5 o największej wartości na jednostkę, znając kategorię obiektu
# Dane znajdują się w folderze "dane" w pliku "zbiór_wejściowy.json" oraz "kategorie.json"
# Wynik przedstaw w czytelnej formie na standardowym wyjściu

import json
class Main:
    CT_TO_OUNCE = 0.00705479239
    G_TO_OUNCE = 0.0352739619

    def __init__(self, categories_path="kategorie.json", items_path="zbiór_wejściowy.json"):
        self.categories: dict = self._load_categories(self._open_json(categories_path))
        self.items: dict = self._open_json(items_path)
        self.mapped_items:list[dict] = self._map_items()

    @staticmethod
    def _open_json(file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def _load_categories(categories_data: dict) -> dict[str, dict[str, int]]:
        parsed_dict: dict = {}
        for item in categories_data:
            if item["Typ"] not in parsed_dict:
                parsed_dict[item["Typ"]] = {}
            parsed_dict[item["Typ"]][item["Czystość"]] = item['Wartość za uncję (USD)']
        return parsed_dict

    def _map_items(self) -> list[dict]:
        mapped_items: list = []
        for item in self.items:
            purity: str = item.get("Czystość")
            name: str = item.get("Typ")
            unit_price: int = self.categories.get(name, {}).get(purity)

            if unit_price is None:
                continue

            oz_weight: float = self._calc_oz_weight(item.get("Masa"))
            item["Cena"]: float = oz_weight * unit_price
            mapped_items.append(item)

        return mapped_items

    def _calc_oz_weight(self, weight: str) -> float:
        if weight.endswith("ct"):
            return float(weight[:-2].replace(",", ".")) * self.CT_TO_OUNCE
        elif weight.endswith("g"):
            return float(weight[:-1].replace(",", ".")) * self.G_TO_OUNCE
        else:
            raise ValueError(f"Unknown weight unit: {weight}")

    def print_top_items(self) -> None:
        items_sorted: list = sorted(self.mapped_items, key=lambda x: x.get("Cena", 0), reverse=True)
        for i, item in enumerate(items_sorted[:5], start=1):
            print(f"{i}:")
            for key, value in item.items():
                print(f"\t{key}: {value}")
            print("\n")


if __name__ == '__main__':
    main = Main("kategorie.json", "zbiór_wejściowy.json")
    main.print_top_items()
