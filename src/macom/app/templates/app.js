// Fields Predefinidos

var fieldFullName = {
  name : "full_name",
  title : "Nombre"
};

var fieldDescription = {
  name : "description",
  title : "Descripci&oacute;n"
};

var fieldGoal = {
  name : "goal",
  title : "Objetivo"
};

var fieldReferents = {
  name : "referents",
  title : "Referentes"
};

var fieldDocumentation = {
  name : "documentation",
  title : "Documentaci&oacute;n"
};

var fieldTechnology = {
  name : "technology",
  title : "Tecnolog&iacute;a",
  width : "100"
};

var fieldDirection = {
  name : "direction",
  title : " ",
  width : "20",
  type : "image",
  imageURLPrefix : "/media/img/icon",
  imageURLSuffix : ".png"
};

var fieldExternal = {
  name : "external",
  title : " ",
  width : "20",
  type : "image",
  imageURLPrefix : "/media/img/external",
  imageURLSuffix : "-icon.gif"
};

isc.Window.create({
  ID : "modalWindow",
  autoSize : true,
  autoCenter : true,
  width : "95%",
  height : "95%",
  isModal : true,
  showModalMask : true,
  autoDraw : false,
  showMinimizeButton : false,
  items : isc.HTMLPane.create({
    ID : "modalWindowPane",
    width : "100%",
    height : "100%",
    contentsType : "page"
  })
});

isc.DetailViewer.addProperties({
  autoFetchData : true
})

// Objetos predefinidos

isc.defineClass("DetailGrid", "ListGrid").addProperties({
  recordDoubleClick : openTab,
  alternateRecordStyles : true,
  autoFetchData : true,
  showFilterEditor : true,
  filterOnKeypress : true
});

isc.defineClass("DetailGridInterface", "DetailGrid").addProperties({
  fields : [ fieldDirection, fieldFullName, fieldTechnology, fieldGoal ]
});

isc.defineClass("DetailGridDependency", "DetailGrid").addProperties({
  fields : [ fieldDirection, fieldFullName, fieldTechnology, fieldGoal ]
});

isc.defineClass("JsonDataSource", "DataSource").addProperties({
  dataFormat : "json",
  dataProtocol : "getParams"
});

function getIcon( iconSrc ){
    return isc.Canvas.imgHTML( iconSrc, 16, 16 );
}

function getIconByKind(node) {
  return "/media/img/" + node.kind + (node.external ? "-external" : "") + ".png";
}

// Custom controls

isc.defineClass("Diagram", "VLayout").addProperties({
  height : "*",
  diagramRenderServiceURL : "{{diagram_service_url}}/",
  initWidget : function() {
    this.diagramSourceURL = window.location.protocol + "//" + window.location.host + this.src;
    this.diagramImageURL = this.diagramRenderServiceURL + this.diagramSourceURL;
    this.diagramImage = isc.Img.create({
        imageType : "normal",
        autoDraw: false
    });
    this.diagramSourceButton = isc.IButton.create({
      title : "View source",
      diagramSourceURL : this.diagramSourceURL,
      click : function() {
        modalWindow.setTitle("Diagram Source");
        modalWindow.show();
        modalWindowPane.setContentsURL(this.diagramSourceURL);
      }
    });
    // Espera que este las dimenciones de la imagen y la impacta en el control de diagrama
    this.checkImgSize = function() {
        var diagram = this;
        var image = new Image();
        image.onload  = function () {
            diagram.diagramImage.setWidth( this.width );
            diagram.diagramImage.setHeight( this.height );
            diagram.diagramImage.setSrc( this.src );
            diagram.diagramImage.draw();
        }
        image.src = this.diagramImageURL;
    }
    this.addMembers([ this.diagramImage, this.diagramSourceButton ]);
    this.checkImgSize();
    return this.Super("initWidget", arguments);
  }
});

isc.defineClass ( "ItemViewer", "VLayout").addProperties({
    title: false,
    data: false,  // Datos a mostrar del item
    fields: false, // Definicion de los fields de la informacion del item
    additionalInfo: false,

    height : "*",
    initWidget : function() {
        // Detalles del Item
        var infoFields = new Array();
        // titulo
        infoFields.push ({ 
            value : ( this.title ? this.title + " ": "")
                    + this.data.full_name
                    + ( this.data.external ? " " + getIcon("/media/img/external-icon.gif") : "")
                    + ( this.data.direction ? " " + getIcon("/media/img/icon" + this.data.direction + ".png") + " " : ""),
            type : "header"
        });
        if ( this.fields ) infoFields = infoFields.concat( this.fields );         // Definicion de datos
        
        this.detail = isc.DetailViewer.create({
            fields : infoFields,
            data : this.data
        });
        
        // Spacer
        this.spacer = isc.LayoutSpacer.create({ height : "10" });

        // Tabs de informacion
        var tabsInfo = new Array();

        if ( this.data.diagram_uri ){
            tabsInfo.push ( {
                title : "Diagrama",
                pane : isc.Diagram.create({
                    ID : this.data.full_name + "_" + this.ID,
                    src : this.data.diagram_uri
                })
            });
        }
        if ( this.additionalInfo ) tabsInfo = tabsInfo.concat ( this.additionalInfo );
        
        this.tabs = isc.TabSet.create({
            tabs : tabsInfo
        });
        
        this.addMembers ( [ this.detail, this.spacer, this.tabs ] );
        
        return this.Super("initWidget", arguments);
    }
});

// APPLICATION

function openTab(viewer, record, recordNum, field, fieldNum, value, rawValue) { // buscar tab q tenga el mismo record
  var tab = ContentTabSet.getTab(record.resource_uri);

  // si no se encuentra generar uno nuevo con titulo = record.name
  if (tab == null || typeof (tab) == 'undefined') {
    ContentTabSet.addTab({
      ID : record.resource_uri,
      title : getIcon(getIconByKind(record)) + "  "
          + (record.full_name.length > 40 ? "... " + record.full_name.substring(record.full_name.length - 40) : record.full_name),
      record : record
    });

    // Busca el tab recien creado
    tab = ContentTabSet.getTab(record.resource_uri);

    // Se fija el record.kind
    switch (record.kind) {
      case 'root': // Si es root:
        // muetra items del root
        showViewRoot(tab, record);
        break;

      default: // Si es system, module, dependency o interface
        // DATASOURCE
        isc.JsonDataSource.create({
          ID : record.resource_uri,
          dataURL : record.resource_uri
        });

        // VIEW
        isc.DataSource.get(record.resource_uri).fetchData(
            null,
            "showView" + record.kind.charAt(0).toUpperCase() + record.kind.slice(1).toLowerCase() + "(data, \""
                + record.resource_uri + "\")" // Callback
        );
    }
  }
  ContentTabSet.selectTab(tab);
}

function showViewRoot(tab, record) {
  var tabset = new Array();

  for ( var i = 0; i < record.diagrams.length; i++) {
    tabset.push({
      title : record.diagrams[i].name,
      pane : isc.Diagram.create({
        src : record.diagrams[i].diagram_uri
      })
    })
  }

  tab.setPane(isc.TabSet.create({
    tabs : tabset
  }));
}

function showViewSystem(data, id) {
  // Variables de datos
  var modules = data[0].modules;
  var module_interfaces = new Array();
  for ( var i = 0; i < modules.length; i++) {
    if (modules[i].interfaces != null) {
      for ( var j = 0; j < modules[i].interfaces.length; j++) {
        module_interfaces.push(modules[i].interfaces[j]);
      }
    }
  }

  // Representacion
  var system = data[0];
  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
    title : "Sistema",
    data : system,
    fields : [ fieldDescription, fieldReferents, fieldDocumentation ],
    additionalInfo: [{
        title : "M&oacute;dulos (" + modules.length + ")",
        pane : isc.DetailGrid.create({
          ID : "systemModules" + system.full_name,
          data : modules,
          fields : [ fieldExternal, fieldFullName, fieldGoal ]
        })
    }, {
        title : "Interfaces (" + module_interfaces.length + ")",
        pane : isc.DetailGridInterface.create({
          ID : "systemInterfaces" + system.full_name,
          data : module_interfaces
        })
    }, {
        title : "Dependencias (" + system.dependencies.length + ")",
        pane : isc.DetailGridDependency.create({
          ID : "systemDependencies" + system.full_name,
          data : system.dependencies
        })
    }, {
        title : "Dependencias desde otros sistemas (" + system.dependents.length + ")",
        pane : isc.DetailGridDependency.create({
          ID : "systemDependents" + system.full_name,
          data : system.dependents
        })
    }]
  }));
}

function showViewModule(data, id) {
  var module = data[0];
  ContentTabSet.getTab(id).setPane( isc.ItemViewer.create({
    title : "M&oacute;dulo",
    data : module,
    fields : [ fieldGoal, fieldReferents, fieldDocumentation ],
    additionalInfo: [{
        title : "Interfaces (" + module.interfaces.length + ")",
        pane : isc.DetailGridInterface.create({
          ID : "moduleInterfaces" + module.full_name,
          data : module.interfaces
        })
    }] 
  }));
}

function showViewInterface(data, id) {
  ContentTabSet.getTab(id).setPane( isc.ItemViewer.create({
    title : "Interface",
    data : data[0],
    fields : [ fieldGoal, fieldReferents, fieldDocumentation, fieldTechnology ]
  }));
}

function showViewDependency(data, id) {
  ContentTabSet.getTab(id).setPane( isc.ItemViewer.create({
    title : "Dependencia",
    data : data[0],
    fields : [ fieldGoal, fieldReferents, fieldDocumentation, fieldTechnology ],
    additionalInfo: [{
        title : "Interfaz utilizada",
        pane : isc.DetailGridInterface.create({
          data : new Array(data[0].interface)
        })
    }] 
  }));
}

// Layout principal

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
      imageType : "natural",
      src : "grass.png",
    }) ]
  }), isc.HLayout.create({
    ID : "ContentSection",
    height : "*",
    showEdges : "true",
    members : [ isc.TreeGrid.create({
      ID : "NavigationTree",
      width : 300,
      dataSource : isc.JsonDataSource.create({
        dataURL : "{% url api_model %}",
        fields : [ {
          name : "name",
          title : "Sistemas"
        }, ]
      }),
      autoFetchData : true,
      dataProperties : {
        openProperty : "isOpen"
      },
      loadDataOnDemand : false,
      defaultIsFolder : false,
      showResizeBar : true,
      generateClickOnEnter : true,
      getIcon : function(node) {
        return getIconByKind(node);
      },
      dataSource : isc.JsonDataSource.create({
        dataURL : "{% url api_model %}",
        fields : [ {
          name : "name"
        } ]
      }),
      dataArrived : function(p) {
        openTab(null, p.children[0]);
      },
      fields : [ {
        name : "name",
        recordDoubleClick : openTab
      } ],
      recordDoubleClick : function() {
        // Elimina el evento de dobleClick por default
      }
    }), isc.TabSet.create({
      ID : "ContentTabSet",
      canCloseTabs : true,
      closeTabIconSize : 12
    }) ]
  }) ]
});
