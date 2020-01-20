<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <q-page>
    <div class="row">
      <div class="col-lg-3 q-pa-sm">
        <q-toolbar>
          <q-btn round icon="add"/>
        </q-toolbar>
        <q-scroll-area style="height: 800px;">
          <q-list bordered>
            <q-item v-for="col in columns.slice(1)" v-bind:key="col.name" clickable>
              <q-item-section top>
                <q-item-label lines="1">
                  <span class="text-grey-10">{{ col.label }}</span>
                </q-item-label>
                <q-item-label caption lines="1">
                  {{ col.params }}
                </q-item-label>
                <q-item-label lines="1" class="q-mt-xs">
                  {{ col.norms }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                  <div class="col-sm">mid</div>
                  <div class="col-sm">spread</div>
                  <div class="col-sm">step</div>
              </q-item-section>
              <q-item-section side>
                <div class="text-grey-8 q-gutter-xs">
                  <q-btn class="gt-xs" size="12px" flat dense round icon="edit" @click="onEditColumn(col)"/>
                  <q-btn class="gt-xs" size="12px" flat dense round icon="delete" @click="onDeleteColumn(col)"/>
                </div>
              </q-item-section>
            </q-item>

            <q-separator/>

          </q-list>
        </q-scroll-area>
      </div>
      <div class="col-lg-9 q-pa-sm">
        <q-table
          title="Отчёт"
          dense
          :data="data"
          :columns="columns"
          row-key="name"
        >
          <template v-slot:header-cell="props">
            <q-th :props="props">
              {{ props.col.label }}<br/>
              {{ props.col.params }}<br/>
              {{ props.col.norms }}
            </q-th>
          </template>
        </q-table>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  data () {
    return {
      leftDrawer: true,
      columns: [
        { name: 1, label: '№ миксросхемы', norms: 'Норма', params: 'Параметры', field: 'name', align: 'left' },
        {
          name: 1,
          label: 'F1, ГГц\nUп = 4,5В',
          required: true,
          align: 'left',
          field: row => row[0],
          params: 'Uп = 4,5В',
          norms: 'не более 1,9'
        },
        { name: 2, label: 'f2, ГГЦ', field: row => row[1], align: 'center', params: 'Uп = 4.5 В', norms: 'не менее 12,3' },
        { name: 3, label: 'D, дБ', field: row => row[2], params: 'Uп = 4.5 В', norms: 'не менее 51' },
        { name: 4, label: 'Pвх мин, дБм', field: row => row[3], params: 'Uп = 4.5 В', norms: 'не более -41' },
        { name: 5, label: 't1, нс', field: row => row[4], params: 'Uп = 4.5 В', norms: 'не более 25' },
        { name: 6, label: 'I, мА', field: row => row[5], params: 'Uп = 5.5 В', norms: 'не более 100' }
      ],
      data: [
        {
          name: 1,
          0: 1.5,
          1: 12.8,
          2: 56.0,
          3: -44,
          4: 20,
          5: 34
        },
        {
          name: 2,
          0: 1.6,
          1: 12.9,
          2: 57.0,
          3: -47,
          4: 23,
          5: 36
        }
      ]
    }
  }
}
</script>
