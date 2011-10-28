// UTILS

String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase();
}

// INTERFACE

isc.DataSource.create({
	ID : "ds_model",
	dataURL : "{% url api_model %}",
	dataFormat : "json",
	fields : [ {
		name : "name"
	 }, ]
 });

isc.VLayout.create({
	width : "100%",
	height : "100%",
	members : [ isc.HStack.create({
		ID : "HeaderSection",
		height : 48,
		hPolicy : "fill",
		members : [ isc.Label.create({
			contents : "macom",
			baseStyle : "header"
		 }), isc.LayoutSpacer.create({
			width : "*"
		 }), isc.Img.create({
			src : "grass.png",
			imageType : "normal"
		 }) ]
	 }), isc.HLayout.create({
		ID : "ContentSection",
		height : "*",
		showEdges : "true",
		members : [ isc.TreeGrid.create({
			ID : "NavigationTree",
            width : 300,
			dataSource : "ds_model",
			autoFetchData : true,
			loadDataOnDemand : false,
			defaultIsFolder : false,
			showResizeBar : true,
			generateClickOnEnter : true,
			fields : [ {
				name : 'name',
				recordDoubleClick : openTab
			 } ],
		 }), isc.TabSet.create({
			ID : 'ContentTabSet'
		 }) ]
	 }), isc.HStack.create({
		ID : "FooterSection",
		height : "1",
		members : [ isc.IButton.create({
			title : "Console",
			click : "isc.showConsole()"
		 }) ]
	 }) ]
 });

function openTab(viewer, record, recordNum, field, fieldNum, value, rawValue) {
	// buscar tab q tenga el mismo record
    var tab = ContentTabSet.getTab(record.id);

	// si no se encuentra generar uno nuevo con titulo = record.name
	if ( tab == null || typeof (tab) == 'undefined') {
        ContentTabSet.addTab({
			ID: record.id,
            title : ( record.full_name.length > 40 ? "... " + record.full_name.substring(record.full_name.length - 40) : record.full_name ),
			record : record,
			canClose : true,
		});
        // Busca el tab recien creado
		tab = ContentTabSet.getTab(record.id);
        
        // Crea el datasource
        createDS(record);
        
        // Llena los datos segun el tipo
        isc.DataSource.get(record.id).fetchData(null, "process"+record.kind.capitalize()+"(data, \""+ record.id +"\")");

	 }
	ContentTabSet.selectTab(tab);
 }

 function createDS(record){
    isc.DataSource.create({
        ID : record.id,
        dataURL : record.id,
        dataFormat : "json",
        dataProtocol : "getParams",
        fields : [
            { name : "external", valueMap : { false:"No", true :"Sí" } },
            { name : "kind", valueMap : { system:"Sistema", module:"Módulo", interface:"Interfaz" } }
        ]
    });
}

 function processSystem(data, id){
    var system = data[0];
    var modules = system.modules;

    var module_interfaces = new Array();
    for (var i =0; i<modules.length; i++) {
/*
        if ( modules[i].dependencies != null ) {
            for (var j =0; j<modules[i].dependencies.length; j++) {
                module_dependencies.push(modules[i].dependencies[j]);
            }
        }
*/
        if ( modules[i].interfaces != null ) {
            for (var j =0; j<modules[i].interfaces.length; j++) {
                module_interfaces.push(modules[i].interfaces[j]);
            }
        }
    }

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [ 
                isc.Label.create( {contents: system.kind , height: 1 } ),
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data: system,
                    fields : [
                        { name : "name", title : "Nombre" },
                        { name : "description", title : "Descripción" },
                        { name : "referents", title : "Referentes" },
                        { name : "documentation", title : "Documentación" },
                        { name : "external", title : "Externo" }
                    ]
                }),
                isc.LayoutSpacer.create( {height:"10" } ),
                isc.TabSet.create({
                    tabs: [ {
                        title: "Módulos (" + modules.length + ")", 
                        pane: isc.ListGrid.create({
                            autoFetchData : true,
                            data : modules,
                            fields : [
                                { name : "full_name", title : "Nombre" },
                                { name : "goal", title : "Objetivo" },
                                { name : "external", title : "Externo", width: "50" }
                            ] })
                        }, {
                        title: "Interfaces (" + module_interfaces.length + ")", 
                        pane: isc.ListGrid.create({
                            autoFetchData : true,
                            data : module_interfaces,
                            fields : [
                                { name : "full_name", title : "Nombre" },
                                { name : "goal", title : "Objetivo" },
                                { name : "technology", title : "Tecnología", width: "100" },
                                { name : "direction", title : "Dirección", width: "60" }
                            ] })
                        }, {
                        title: "Dependencias (" + system.dependencies.length + ")", 
                        pane: isc.ListGrid.create({
                            autoFetchData : true,
                            data : system.dependencies,
                            fields : [
                                { name : "full_name", title : "Nombre" },
                                { name : "goal", title : "Objetivo" },
                                { name : "technology", title : "Tecnología", width: "100" },
                                { name : "direction", title : "Dirección", width: "60" }
                            ] })
                        }, {
                        title: "Dependencias desde otros sistemas (" + system.dependents.length + ")", 
                        pane: isc.ListGrid.create({
                            autoFetchData : true,
                            data : system.dependents,
                            fields : [
                                { name : "full_name", title : "Nombre" },
                                { name : "goal", title : "Objetivo" },
                                { name : "technology", title : "Tecnología", width: "100" },
                                { name : "direction", title : "Dirección", width: "60" }
                            ] })
                        }
                    ]
                })
            ]
        })
    );
}

function processModule( data, id ){
         ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    autoFetchData : true,
                     data: data[0],
                    fields : [
                        { name : "kind", title : "Tipo" },
                        { name : "full_name", title : "Nombre" },
                        { name : "goal", title : "Objetivo" },
                        { name : "referents", title : "Referentes" }, 
                        { name : "documentation", title : "Documentación" },
                        { name : "external", title : "Externo" },
                        { name : "criticity", title : "Criticidad" }
                    ]
                }),
                isc.LayoutSpacer.create( {height:"10" } ),
                isc.Label.create({
                    contents: "Interfaces",
                    height: "1"
                }),
                isc.ListGrid.create({
                    autoFetchData : true,
                    data : data[0].interfaces,
                    fields : [
                        { name : "full_name", title : "Nombre" },
                        { name : "goal", title : "Objetivo" },
                        { name : "direction", title : "Dirección" },
                        { name : "technology", title : "Tecnología" },
                        { name : "documentation", title : "Documentación" },
                        { name : "referents", title : "Referentes" },
                        { name : "external", title : "Externo", width: "50" }
                    ]
                })
            ]
        }));
 }

function processInterface( data, id ){
     ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: isc.DetailViewer.create({
                autoFetchData : true,
                data : data[0],
                fields : [
                    { name : "kind", title : "Tipo", valueMap : { system:"Sistema", module:"Módulo", interface:"Interfaz" } },
                    { name : "full_name", title : "Nombre" }, 
                    { name : "goal", title : "Objetivo" },
                    { name : "referents", title : "Referentes" },
                    { name : "documentation", title : "Documentación" },
                    { name : "technology", title : "Tecnología" },
                    { name : "direction", title : "Dirección" }
                ]
             })
    }));
 }
