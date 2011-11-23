isc.defineClass("DetailGrid", "ListGrid").addProperties({
  alternateRecordStyles : true,
  autoFetchData : true,
  showFilterEditor : true,
  filterOnKeypress : true
});

isc.defineClass("InterfaceDetailGrid", "DetailGrid").addProperties({
  fields : [ mcm.fields.Direction, mcm.fields.FullName, mcm.fields.Technology, mcm.fields.Goal ]
});

isc.defineClass("DependencyDetailGrid", "DetailGrid").addProperties({
  fields : [ mcm.fields.Direction, mcm.fields.FullName, mcm.fields.Technology, mcm.fields.Goal ]
});

isc.defineClass("JSONDataSource", "DataSource").addProperties({
  dataFormat : "json",
  dataProtocol : "getParams"
});

isc.defineClass("Diagram", "VLayout").addProperties({
  height : "*",
  diagramRenderServiceURL : "{{diagram_service_url}}/",
  initWidget : function() {
    this.diagramSourceURL = window.location.protocol + "//" + window.location.host + this.src;
    this.diagramImageURL = this.diagramRenderServiceURL + this.diagramSourceURL;
    this.diagramSourceButton = isc.IButton.create({
      title : "View source",
      diagramSourceURL : this.diagramSourceURL,
      click : function() {
        mcm.showSource("Diagram Source", this.diagramSourceURL);
      }
    });
    this.diagramContainer = isc.HStack.create();
    this.addMembers([ this.diagramContainer, this.diagramSourceButton ]);
    var image = new Image();
    image.diagram = this;
    image.onload = function() {
      this.diagram.diagramImage = isc.Img.create({
        imageType : "normal",
        width : this.width,
        height : this.height,
        src : this.src
      });
      this.diagram.diagramContainer.addMember(this.diagram.diagramImage);
    }
    image.src = this.diagramImageURL;
    return this.Super("initWidget", arguments);
  }
});

isc.defineClass("ItemViewer", "VLayout").addProperties({
      title : false,
      data : false, // Datos a mostrar del item
      fields : false, // Definicion de los fields de la informacion del item
      additionalInfo : false,
      height : "*",
      initWidget : function() {
        // Detalles del Item
        var infoFields = new Array();
        // titulo
        infoFields.push({
          value : (this.title ? this.title + " " : "") + this.data.full_name
              + (this.data.external ? " " + getIcon("/media/img/external-icon.gif") : "")
              + (this.data.direction ? " " + getIcon("/media/img/icon" + this.data.direction + ".png") + " " : ""),
          type : "header"
        });
        if (this.fields) infoFields = infoFields.concat(this.fields); // Definicion de datos
        this.detail = isc.DetailViewer.create({
          autoFetchData : true,
          fields : infoFields,
          data : this.data
        });
        // Spacer
        this.spacer = isc.LayoutSpacer.create({
          height : "10"
        });
        // Tabs de informacion
        var tabsInfo = new Array();
        if (this.data.diagram_uri) {
          tabsInfo.push({
            title : "Diagrama",
            pane : isc.Diagram.create({
              ID : this.data.full_name + "_" + this.ID,
              src : this.data.diagram_uri
            })
          });
        }
        if (this.additionalInfo) tabsInfo = tabsInfo.concat(this.additionalInfo);
        this.tabs = isc.TabSet.create({
          tabs : tabsInfo
        });
        this.addMembers([ this.detail, this.spacer, this.tabs ]);
        return this.Super("initWidget", arguments);
      }
    });

isc.defineClass("SourceViewer", "Window").addProperties({
  autoCenter : true,
  isModal : true,
  showModalMask : true,
  showMinimizeButton : false,
  width : "90%",
  height : "90%",
  items : isc.Layout.create({
    hPolicy : "fill",
    vPolicy : "fill",
    members : isc.HTMLPane.create({
      contentsType : "page"
    })
  }),
  initWidget : function() {
    this.items.members[0].setContentsURL(this.sourceURL);
    return this.Super("initWidget", arguments);
  }
});

mcm.showSource = function(title, sourceURL) {
  isc.SourceViewer.create({
    title : title,
    sourceURL : sourceURL
  })
}
