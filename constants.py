# coding: utf-8
validColors = ("White", "Black", "Green", "Blue", "Red", "Yellow")
validShapes = ("Circle", "Square", "Triangle")

countries = {"Oceania": ("Sumatra", "Borneo", "Nova Guiné", "Austrália"),
			"América do Norte": ("Alaska", "Mackenzie", "Groenlândia",
								"Vancouver", "Ottawa", "Labrador", "Califórnia",
								"Nova York", "México"),
			"América do Sul": ("Colômbia", "Bolívia", "Brasil", "Argentina"),
			"Europa": ("Islândia", "Suécia", "Moscou", "Inglaterra",
						"Alemanha",	"Espanha", "Polônia"),
			"África": ("Argélia", "Egito", "Sudão", "Congo",
						"África do Sul", "Madagascar"),
			"Ásia": ("Oriente Médio", "Aral", "Omsk", "Dudinka", "Sibéria",
					"Tchita", "Vladvostok", "Mongólia", "Japão", "China",
					"Índia", "Vietnã")}
				
territoryLinks = (("Brasil", "Argentina"),
				("Brasil", "Bolívia"),
				("Brasil", "Colômbia"),
				("Brasil", "Argélia"),
				("Bolívia", "Colômbia"),
				("Bolívia", "Argentina"),
				("Colômbia", "México"),
				("México", "Nova York"),
				("México", "Califórnia"),
				("Nova York", "Califórnia"),
				("Califórnia", "Vancouver"),
				("Califórnia", "Ottawa"),
				("Nova York", "Ottawa"),
				("Nova York", "Labrador"),
				("Ottawa", "Labrador"),
				("Vancouver", "Ottawa"),
				("Vancouver", "Alaska"),
				("Vancouver", "Mackenzie"),
				("Alaska", "Mackenzie"),
				("Ottawa", "Mackenzie"),
				("Labrador", "Groenlândia"),
				("Mackenzie", "Groenlândia"),
				("Groenlândia", "Islândia"),
				("Alaska", "Vladivostok"),
				("Islândia", "Inglaterra"),
				("Inglaterra", "Suécia"),
				("Inglaterra", "Alemanha"),
				("Inglaterra", "Espanha"),
				("Espanha", "Alemanha"),
				("Espanha", "Polônia"),
				("Polônia", "Alemanha"),
				("Polônia", "Moscou"),
				("Moscou", "Suécia"),
				("Moscou", "Omsk"),
				("Moscou", "Aral"),
				("Moscou", "Oriente Médio"),
				("Polônia", "Oriente Médio"),
				("Polônia", "Egito"),
				("Espanha", "Egito"),
				("Espanha", "Argélia"),
				("Argélia", "Egito"),
				("Argélia", "Sudão"),
				("Egito", "Sudão"),
				("Argélia", "Congo"),
				("Sudão", "Congo"),
				("Congo", "África do Sul"),
				("África do Sul", "Madagascar"),
				("Sudão", "Madagascar"),
				("Oriente Médio", "Egito"),
				("Oriente Médio", "Aral"),
				("Oriente Médio", "Índia"),
				("Aral", "Índia"),
				("Aral", "Omsk"),
				("Aral", "China"),
				("Índia", "China"),
				("Índia", "Vietnã"),
				("Vietnã", "China"),
				("China", "Omsk"),
				("China", "Mongólia"),
				("China", "Japão"),
				("Omsk", "Dudinka"),
				("Dudinka", "Mongólia"),
				("Mongólia", "Tchita"),
				("Dudinka", "Tchita"),
				("Dudinka", "Sibéria"),
				("Sibéria", "Tchita"),
				("Tchita", "Vladivostok"),
				("Sibéria", "Vladivostok"),
				("China", "Vladivostok"),
				("Japão", "Vladivostok"),
				("Índia", "Sumatra"),
				("Vietnã", "Borneo"),
				("Borneo", "Nova Guiné"),
				("Borneo", "Austrália"),
				("Austrália", "Nova Guiné"),
				("Austrália", "Sumatra"))

debug = True
