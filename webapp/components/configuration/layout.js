export default {
  global: {
    sideBorders: 8,
    tabSetHeaderHeight: 26,
    tabSetTabStripHeight: 26,
  },
  layout: {
    type: 'tabset',
    weight: 100,
    id: 'root',
    children: [
      {
        type: 'row',
        weight: 20,
        children: [
          {
            type: 'tabset',
            weight: 100,
            id: 'leftPanel',
            enableDeleteWhenEmpty: false,
            enableDrop: false,
            enableDrag: false,
            enableDivide: false,
            enableMaximize: false,
            children: [],
          },
        ],
      },
      {
        type: 'row',
        weight: 60,
        children: [
          {
            type: 'tabset',
            weight: 60,
            id: 'rightTop',
            enableDeleteWhenEmpty: false,
            children: [],
          },
          {
            type: 'tabset',
            weight: 40,
            id: 'bottomPanel',
            enableDeleteWhenEmpty: false,
            children: [],
          },
        ],
      },

    ],
  },
  borders: [
    {
      type: 'border',
      location: 'bottom',
      size: 100,
      children: [],
      barSize: 10,
    },
  ],
};
