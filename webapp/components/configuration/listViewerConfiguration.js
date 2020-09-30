import { GroupComponent } from "@geppettoengine/geppetto-ui/list-viewer/ListViewer";
import { FILEVARIABLE_LENGTH } from "../constants";
import { CustomIconComponent } from "../CustomIconComponent";
import ListControlsComponent from "../ListMenuComponent";

const conf = [
  {
    id: "controls",
    title: "Controls",
    customComponent: GroupComponent,

    configuration: [
      {
        id: "showPlot",
        customComponent: CustomIconComponent,
        visible: (entity) =>
          Instances.getInstance(entity.path + ".data") &&
          Instances.getInstance(entity.path + ".timestamps"),

        source: (entity) => entity,
        configuration: {
          action: "clickShowPlot",
          label: "Plot",
          tooltip: "Plot time series",
          color: "rgba(255, 255, 255, 0.3)",
          defaultColor: (entity) => Instances.getInstance(entity.path).color,
        },
      },
      {
        id: "image",
        customComponent: CustomIconComponent,
        visible: (entity) => entity.type === "ImageSeries",
        source: (entity) => entity,
        configuration: {
          action: "clickShowImg",
          icon: "picture-o",
          label: "Plot",
          tooltip: "Plot image series",
          color: "rgba(255, 255, 255, 0.3)",
        },
      },
      {
        id: "menuOptions",
        customComponent: ListControlsComponent,
        source: (entity) => entity,
        configuration: {
          actions: "clickShowDetails",
          label: "Show details",
          tooltip: "Show details",
          color: "#ffffff",
        },
      },
    ],
  },
  {
    id: "path",
    title: "Path",
    source: ({ path }) => path.slice(FILEVARIABLE_LENGTH),
  },
  {
    id: "type",
    title: "Type",
    source: "type",
  },
  {
    id: "description",
    title: "Description",
    source: "description",
  },
];

export default conf;
