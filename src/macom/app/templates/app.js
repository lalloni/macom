//Settings
var diagramServiceUrl = "{{diagram_service_url}}/{{localuri}}";
diagramServiceUrl = diagramServiceUrl.substring(0,diagramServiceUrl.length-1); // Le saca la / del final

// Fields Predefinidos
var fieldName = { name : "full_name", title : "Nombre" };
var fieldDescription = { name : "description", title : "Descripci&oacute;n" };
var fieldGoal = { name : "goal", title : "Objetivo" };
var fieldReferents = { name : "referents", title : "Referentes" };
var fieldDocumentation = { name : "documentation", title : "Documentaci&oacute;n" };
var fieldTechnology = { name : "technology", title : "Tecnolog&iacute;a", width: "100" };
var fieldDirection = { name : "direction", title : "Direcci&oacute;n", width: "60", type:"image", imageURLPrefix:"/media/img/morocho/icon", imageURLSuffix:".png" };
var fieldExternal =  { name : "external", title : "Externo", width: "50", type:"image", imageURLPrefix:"/media/img/", imageURLSuffix:"-icon.gif"};

var fieldsBasic =  [fieldName, fieldGoal, fieldReferents, fieldDocumentation];

// Conjunto de fields por tipo
var fieldsSystem = [fieldName, fieldDescription, fieldReferents, fieldDocumentation,fieldExternal]
var fieldsModule = fieldsBasic.concat(fieldExternal);
var fieldsInterface = fieldsBasic.concat([fieldTechnology, fieldDirection]);

// Objetos predefinidos
isc.defineClass("DetailGrid", "ListGrid");
isc.DetailGrid.addProperties({
    recordDoubleClick: openTab,
    alternateRecordStyles:true,
    autoFetchData : true,
    showFilterEditor: true,
    filterOnKeypress: true,
    canExpandRecords: true,
    expansionMode: "details"
});

isc.defineClass("InterfaceDataSource", "DataSource");
isc.InterfaceDataSource.addProperties({
        clientOnly: true,
        fields : fieldsInterface
});

// APPLICATION

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
                showViewRoot(tab, record);
                break;
            
            default: // Si es system, module, dependency o interface
                // DATASOURCE
                isc.DataSource.create({
                    ID : record.resource_uri,
                    dataURL : record.resource_uri,
                    dataFormat : "json",
                    dataProtocol : "getParams"
                });
                
                // VIEW
                isc.DataSource.get(record.resource_uri)
                    .fetchData(null,
                                    "showView"+record.kind.charAt(0).toUpperCase() + record.kind.slice(1).toLowerCase()+"(data, \""+ record.resource_uri +"\")" // Callback
                );
        }
	 }
	ContentTabSet.selectTab(tab);
 }


function showViewRoot ( tab, record ){
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
                    src: diagramServiceUrl+tabs[i].diagram_uri,
                    imageType : "natural"
            })
        })
    }

    return tabset;
}

function showViewSystem(data, id){
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
                    fields : [{ value : "Sistema", type : "header"}].concat(fieldsSystem)
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [ {
                        title: "Diagrama",
                        pane: isc.Img.create({
                            src: diagramServiceUrl+system.diagram_uri,
                            imageType : "natural"
                            })
                        }, {
                            title: "M&oacute;dulos (" + modules.length + ")", 
                            pane: isc.DetailGrid.create({
                                dataSource : isc.DataSource.create({
                                    testData: modules,
                                    clientOnly: true,
                                    fields : fieldsModule
                                }),
                                fields : [
                                    { name : "full_name" }, { name : "external" }
                                ]
                            })
                        }, {
                            title: "Interfaces (" + module_interfaces.length + ")", 
                            pane: isc.DetailGrid.create({
                                dataSource :  isc.InterfaceDataSource.create({
                                    testData: module_interfaces
                                }) ,
                                fields : [ { name : "full_name" }, { name : "technology"}, { name : "direction" } ] 
                            })
                        }, {
                            title: "Dependencias (" + system.dependencies.length + ")", 
                            pane: isc.DetailGrid.create({
                                ID: "Dependencies",
                                dataSource :  isc.InterfaceDataSource.create({
                                    testData: system.dependencies
                                }) ,
                                fields : [ { name : "full_name" }, { name : "technology"}, { name : "direction" } ] 
                            })
                        }, {
                            title: "Dependencias desde otros sistemas (" + system.dependents.length + ")", 
                            pane: isc.DetailGrid.create({
                                ID: "Dependents",
                                dataSource :  isc.InterfaceDataSource.create({
                                    testData: system.dependents
                                }) ,
                                fields : [ { name : "full_name" }, { name : "technology"}, { name : "direction" } ] 
                            })
                        }
                    ]
                })
            ]
        })
    );
}

function showViewModule( data, id ){
    var module = data[0];

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data: module,
                    fields : [{ value : "M&oacute;dulo", type : "header"}].concat(fieldsModule)
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Diagrama",
                        pane: isc.Img.create({
                            src: diagramServiceUrl+module.diagram_uri,
                            imageType : "natural"
                            })
                        }, {
                        title: "Interfaces (" + module.interfaces.length + ")", 
                        pane: isc.DetailGrid.create({
                            dataSource :  isc.InterfaceDataSource.create({
                                testData: module.interfaces
                            }) ,
                            fields : [ { name : "full_name" }, { name : "technology"}, { name : "direction" } ] 
                        })
                    }]
                })
            ]
        })
    );
 }

function showViewInterface( data, id ){
    var interface = data[0];

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data : interface,
                    fields : [{ value : "Interface", type : "header"}].concat(fieldsInterface)
                 }) ,
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Diagrama",
                        pane: isc.Img.create({
                            src: diagramServiceUrl+interface.diagram_uri,
                            imageType : "natural"
                        })
                    }]
                })
            ]
        })
    );
 }

function showViewDependency( data, id ){
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
                    fields : [{ value : "Dependencia", type : "header"}].concat(fieldsInterface)
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.DetailViewer.create({
                    autoFetchData : true,
                    data : interface,
                    recordDoubleClick: openTab,
                    fields : [{ value : "Interfaz utilizada", type : "header"}].concat(fieldsInterface)
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
