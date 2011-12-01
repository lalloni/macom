var app = {};

// Objetos predefinidos

function getIcon(iconSrc) {
  return isc.Canvas.imgHTML(iconSrc, 16, 16);
}

function getIconByKind(node) {
  return "/media/img/" + node.kind + (node.external ? "-external" : "") + ".png";
}

// Fields Defaults de aplicacion
app.fields = {
	InterfaceGridFields : [ mcm.fields.Direction, mcm.fields.FullName, mcm.fields.Technology, mcm.fields.Goal, mcm.fields.Published ],
	DependencyGridFields: [ mcm.fields.Direction, mcm.fields.FullName, mcm.fields.Technology, mcm.fields.Goal ]
}

app.views = {
	showRoot: function (tab, record) {
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
	},
	
	showSystem: function (data, id) {
	  // Representacion
	  var system = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Sistema",
	    data : system,
	    fields : [ mcm.fields.Description, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation ],
	    additionalInfo : [ {
	      title : "M&oacute;dulos ",
	      pane : isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
	          dataURL : system.modules_uri,
	          autoFetchData : true,
	          fields : [ mcm.fields.External, mcm.fields.FullName, mcm.fields.Goal ]
	        }),
	      })
	    }, {
	      title : "Interfaces",
	      pane : isc.DetailGrid.create({
	    	initialCriteria: { published: true },  	
	    	dataSource : isc.JSONDataSource.create({
	          dataURL : system.interfaces_uri,
	          autoFetchData : true,
	          cacheAllData: true, // Se utiliza para que initialCriteria actue al inicio
	          fields : app.fields.InterfaceGridFields
	        })
	      })
	    }, {
	      title : "Dependencias",
	      pane : isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
	          dataURL : system.dependencies_uri,
	          autoFetchData : true,
	          fields : app.fields.DependencyGridFields
	        })
	      })
	    }, {
	      title : "Dependencias inversas",
	      pane : isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
	          dataURL : system.reverse_dependencies_uri,
	          autoFetchData : true,
	          fields : app.fields.DependencyGridFields
	        })
	      })
	    } ]
	  }));
	},
	
	showModule: function (data, id) {
	  var module = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "M&oacute;dulo",
	    data : module,
	    fields : [ mcm.fields.Goal, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation ],
	    additionalInfo : [ {
	      title : "Interfaces",
	      pane : isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
	          dataURL : module.interfaces_uri,
	          autoFetchData : true,
	          fields : app.fields.InterfaceGridFields
	        })
	      })
	    }, {
	      title : "Dependencias",
	      pane : isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
	          dataURL : module.dependencies_uri,
	          autoFetchData : true,
	          fields : app.fields.DependencyGridFields
	        })
	      })
	    }, {
	      title : "Dependencias inversas",
	      pane : isc.DetailGrid.create({
	        dataSource : isc.JSONDataSource.create({
	          dataURL : module.reverse_dependencies_uri,
	          autoFetchData : true,
	          fields : app.fields.DependencyGridFields
	        })
	      })
	    } ]
	  }));
	},
	
	showInterface: function (data, id) {
	  var interface = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Interface",
	    data : interface,
	    fields : [ mcm.fields.Goal, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation, mcm.fields.Technology, mcm.fields.Published ],
	    additionalInfo : [ {
	        title : "Dependencias inversas",
	        pane : isc.DetailGrid.create({
	          dataSource : isc.JSONDataSource.create({
	            dataURL : interface.reverse_dependencies_uri,
	            autoFetchData : true,
	            fields : app.fields.DependencyGridFields
	          })
	        })
	      } ]
	  }));
	},
	
	showDependency:	function (data, id) {
	  var dependency = data[0];
	  ContentTabSet.getTab(id).setPane(isc.ItemViewer.create({
	    title : "Dependencia",
	    data : dependency,
	    fields : [ mcm.fields.Goal, mcm.fields.FunctionalReferents, mcm.fields.ImplementationReferents, mcm.fields.Documentation, mcm.fields.Technology ],
	    additionalInfo : [ {
	      title : "Interfaz utilizada",
	      pane : isc.DetailGrid.create({
	          dataSource : isc.JSONDataSource.create({
	            dataURL : dependency.interface.resource_uri,
	            autoFetchData : true,
	            fields : app.fields.InterfaceGridFields
	          })
	      })
	    } ]
	  }));
	}
}

// APPLICATION
function openTab(viewer, record, recordNum, field, fieldNum, value, rawValue) {
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
        app.views.showRoot(tab, record);
        break;

      default: // Si es system, module, dependency o interface
        // DATASOURCE
        isc.JSONDataSource.create({
          ID : record.resource_uri,
          dataURL : record.resource_uri
        }).fetchData(
            null,
            "app.views.show" + record.kind.charAt(0).toUpperCase() + record.kind.slice(1).toLowerCase() + "(data, \""
                + record.resource_uri + "\")" // Callback
        );
    }
  }
  ContentTabSet.selectTab(tab);
}

isc.DetailGrid.addProperties({
  recordDoubleClick : openTab
});



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
      autoFetchData : true,
      loadDataOnDemand : false,
      defaultIsFolder : false,
      showResizeBar : true,
      generateClickOnEnter : true,
      showHeader: false,
        
      dataProperties : {
        openProperty : "isOpen"
      },
      getIcon : function(node) {
        return getIconByKind(node);
      },
      dataSource : isc.JSONDataSource.create({
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
