// UTILS
String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase();
}

function openTab(viewer, record, recordNum, field, fieldNum, value, rawValue) {	// buscar tab q tenga el mismo record
    var tab = ContentTabSet.getTab(record.resource_uri);

	// si no se encuentra generar uno nuevo con titulo = record.name
	if ( tab == null || typeof (tab) == 'undefined') {
        ContentTabSet.addTab({
			ID: record.resource_uri,
            title : ( record.full_name.length > 40 ? "... " + record.full_name.substring(record.full_name.length - 40) : record.full_name ),
			record : record,
			canClose : true
		});
        // Busca el tab recien creado
		tab = ContentTabSet.getTab(record.resource_uri);

        // Se fija el record.kind
        switch (record.kind){
            case 'root': // Si es root:
                // muetra items del root
                processRoot(tab, record);
                break;
            
            default: // Si es system, module, dependency o interface
                // Crea el datasource
                createDS(record);
                
                // Llena los datos segun el tipo
                isc.DataSource.get(record.resource_uri).fetchData(null, "process"+record.kind.capitalize()+"(data, \""+ record.resource_uri +"\")");
        }
	 }
	ContentTabSet.selectTab(tab);
 }

function createDS(record){
    isc.DataSource.create({
        ID : record.resource_uri,
        dataURL : record.resource_uri,
        dataFormat : "json",
        dataProtocol : "getParams"
    });
}

function processRoot ( tab, record ){
    tab.setPane(
        isc.TabSet.create({
            tabs:  getTabs( record.diagrams )
        })
    );
}

function getTabs ( tabs ){
    var tabset = new Array();

    for  ( var i = 0; i < tabs.length; i++ ){
        tabset.push ({
            title: tabs[i].name,
            pane:  isc.Img.create({
                    src: tabs[i].resource_uri,
                    imageType : "natural"
            })
        })
    }

    return tabset;
}

function processSystem(data, id){
    // Variables de datos
    var system = data[0];
    var modules = system.modules;

    var module_interfaces = new Array();
    for (var i =0; i<modules.length; i++) {
        if ( modules[i].interfaces != null ) {
            for (var j =0; j<modules[i].interfaces.length; j++) {
                module_interfaces.push(modules[i].interfaces[j]);
            }
        }
    }

    // Representacion
    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [ 
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data: system,
                    fields : [
                        { value : "Sistema", type : "header"},
                        { name : "full_name", title : "Nombre" },
                        { name : "description", title : "Descripci&oacute;n" },    
                        { name : "referents", title : "Referentes" },
                        { name : "documentation", title : "Documentaci&oacute;n" },
                        { name : "external", title : "Externo" }
                    ]
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [ {
                        title: "M&oacute;dulos (" + modules.length + ")", 
                        pane: isc.ListGrid.create({
                            alternateRecordStyles:true,
                            autoFetchData : true,
                            showFilterEditor: true,
                            filterOnKeypress: true,
                            canExpandRecords: true,
                            expansionMode: "details",
                            dataSource : isc.DataSource.create({
                                testData: modules,
                                clientOnly: true,
                                fields : [
                                    { name : "full_name", title : "Nombre" },
                                    { name : "goal", title : "Objetivo" },
                                    { name : "external", title : "Externo", width: "50" }
                                ] }),
                            recordDoubleClick: openTab,
                            fields : [
                                { name : "full_name", title : "Nombre" }
                            ] })
                        }, {
                        title: "Interfaces (" + module_interfaces.length + ")", 
                        pane: isc.ListGrid.create({
                            alternateRecordStyles:true,
                            autoFetchData : true,
                            recordDoubleClick: openTab,
                            showFilterEditor: true,
                            filterOnKeypress: true,
                            canExpandRecords: true,
                            expansionMode: "details",
                            dataSource :  isc.DataSource.create({
                                testData: module_interfaces,
                                clientOnly: true,
                                fields : [
                                    { name : "full_name", title : "Nombre" },
                                    { name : "goal", title : "Objetivo" },
                                    { name : "technology", title : "Tecnolog&iacute;a", width: "100" },
                                    { name : "direction", title : "Direcci&oacute;n", width: "60" },
                                    { name : "referents", title : "Referentes" },
                                    { name : "documentation", title : "Documentaci&oacute;n" }
                                ]
                            }),
                            fields : [
                                { name : "full_name", title : "Nombre" }
                            ] })
                        }, {
                        title: "Dependencias (" + system.dependencies.length + ")", 
                        pane: isc.ListGrid.create({
                            alternateRecordStyles:true,
                            autoFetchData : true,
                            recordDoubleClick: openTab,
                            showFilterEditor: true,
                            filterOnKeypress: true,
                            canExpandRecords: true,
                            expansionMode: "details",
                            dataSource :  isc.DataSource.create({
                                testData: system.dependencies,
                                clientOnly: true,
                                fields : [
                                    { name : "full_name", title : "Nombre" },
                                    { name : "goal", title : "Objetivo" },
                                    { name : "technology", title : "Tecnolog&iacute;a", width: "100" },
                                    { name : "direction", title : "Direcci&oacute;n", width: "60" },
                                    { name : "referents", title : "Referentes" },
                                    { name : "documentation", title : "Documentaci&oacute;n" }
                                ]
                            }),
                            fields : [
                                { name : "full_name", title : "Nombre" },
                            ] })
                        }, {
                        title: "Dependencias desde otros sistemas (" + system.dependents.length + ")", 
                        pane: isc.ListGrid.create({
                            alternateRecordStyles:true,
                            autoFetchData : true,
                            recordDoubleClick: openTab,
                            showFilterEditor: true,
                            filterOnKeypress: true,
                            canExpandRecords: true,
                            expansionMode: "details",
                            dataSource :  isc.DataSource.create({
                                testData: system.dependents,
                                clientOnly: true,
                                fields : [
                                    { name : "full_name", title : "Nombre" },
                                    { name : "goal", title : "Objetivo" },
                                    { name : "technology", title : "Tecnolog&iacute;a", width: "100" },
                                    { name : "direction", title : "Direcci&oacute;n", width: "60" },
                                    { name : "referents", title : "Referentes" },
                                    { name : "documentation", title : "Documentaci&oacute;n" }
                                ]
                            }),
                            fields : [
                                { name : "full_name", title : "Nombre" },
                            ] })
                        }
                    ]
                })
            ]
        })
    );
}

function processModule( data, id ){
    var module = data[0];

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data: module,
                    fields : [
                        { value : "M&oacute;dulo", type : "header"},    
                        { name : "full_name", title : "Nombre" },
                        { name : "goal", title : "Objetivo" },
                        { name : "referents", title : "Referentes" }, 
                        { name : "documentation", title : "Documentaci&oacute;n" },
                        { name : "external", title : "Externo" },
                        { name : "criticity", title : "Criticidad" }
                    ]
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Interfaces (" + module.interfaces.length + ")", 
                        pane: isc.ListGrid.create({
                            alternateRecordStyles:true,
                            autoFetchData : true,
                            recordDoubleClick: openTab,
                            showFilterEditor: true,
                            filterOnKeypress: true,
                            canExpandRecords: true,
                            expansionMode: "details",
                            dataSource :  isc.DataSource.create({
                                testData: module.interfaces,
                                clientOnly: true,
                                fields : [
                                    { name : "full_name", title : "Nombre" },
                                    { name : "goal", title : "Objetivo" },
                                    { name : "technology", title : "Tecnolog&iacute;a", width: "100" },
                                    { name : "direction", title : "Direcci&oacute;n", width: "60" },
                                    { name : "referents", title : "Referentes" },
                                    { name : "documentation", title : "Documentaci&oacute;n" }
                                ]
                            }),
                            fields : [
                                { name : "full_name", title : "Nombre" }
                            ] 
                        })
                    }]
                })
            ]
        })
    );
 }

function processInterface( data, id ){
    var interface = data[0];

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: isc.DetailViewer.create({
                autoFetchData : true,
                data : interface,
                fields : [
                    { value : "Interfaz", type : "header"},
                    { name : "full_name", title : "Nombre" },
                    { name : "goal", title : "Objetivo" },
                    { name : "referents", title : "Referentes" },
                    { name : "documentation", title : "Documentaci&oacute;n" },
                    { name : "technology", title : "Tecnolog&iacute;a" },
                    { name : "direction", title : "Direcci&oacute;n" }
                ]
             })
    }));
 }

function processDependency( data, id ){
    var dependency = data[0];
    var interface = dependency.interface;

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data: dependency,
                    canExpandRecords: true,
                    expansionMode: "details",
                    fields : [
                        { value : "Dependencia", type : "header"},
                        { name : "full_name", title : "Nombre" },
                        { name : "goal", title : "Objetivo" },
                        { name : "technology", title : "Tecnolig&iacute;a" },
                        { name : "direction", title : "Direcci&oacute;n" },
                    ]
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data : interface,
                    recordDoubleClick: openTab,
                    fields : [
                        { value : "Interfaz utilizada", type : "header"},
                        { name : "full_name", title : "Nombre" },
                        { name : "goal", title : "Objetivo" },
                        { name : "direction", title : "Direcci&oacute;n" },
                        { name : "technology", title : "Tecnolog&iacute;a" },
                        { name : "documentation", title : "Documentaci&oacute;n" },
                        { name : "referents", title : "Referentes" },
                        { name : "external", title : "Externo", width: "50" }
                    ]
                })
            ]
        })
    );
 }

// INTERFACE
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
            dataSource : isc.DataSource.create({
                dataURL : "{% url api_model %}",
                dataFormat : "json",
                fields : [ {
                    name : "name"
                 }]
            }),
            autoFetchData : true,
            dataProperties: {openProperty: "isOpen"},
            loadDataOnDemand : false,
            defaultIsFolder : false,
            showResizeBar : true,
            generateClickOnEnter : true,
            dataArrived: function ( p ) {
                openTab( null, p.children[0] );
            },
            fields : [{
                name : "name",
                recordDoubleClick : openTab
            }]
        }), isc.TabSet.create({
            ID : "ContentTabSet"
        })
        ]
     }), isc.HStack.create({
        ID : "FooterSection",
        height : "1",
        members : [ isc.IButton.create({
            title : "Console",
            click : "isc.showConsole()"
         }) ]
     }) ]
 });
