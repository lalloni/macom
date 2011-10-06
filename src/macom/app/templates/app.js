
isc.DataSource.create({
	ID : "system_list",
	dataURL : "{% url api_system_list %}",
	dataFormat : "json",
	fields : [ {
		name : "name"
	}, {
		name : "description"
	}, ]
});

isc.VLayout.create({
	width : "100%",
	height : "100%",
	members : [ isc.HStack.create({
		ID : "HeaderBar",
		height : "30px",
		members : [ isc.Label.create({
			contents : "macom"
		}) ],
	}), isc.HLayout.create({
		height : "*",
		members : [ isc.ListGrid.create({
			dataSource : "system_list",
			autoFetchData : true,
			showResizeBar : true,
		}), isc.TabSet.create({
			tabs : [ {
				title : "Prueba 1",
				pane : isc.Label.create({
					contents : "Contenido"
				})
			}, {
				title : "Prueba 2",
				pane : isc.Label.create({
					contents : "Contenido"
				})
			}, {
				title : "Prueba 3",
				pane : isc.Label.create({
					contents : "Contenido"
				})
			}, {
				title : "Prueba 4",
				pane : isc.Label.create({
					contents : "Contenido"
				})
			}, ],
		}), ],
	}), isc.HStack.create({
		ID : "BottomToolBar",
		height : "1",
		members : [ isc.IButton.create({
			title : "Console",
			click : "isc.showConsole()"
		}), ]
	}), ]
});
