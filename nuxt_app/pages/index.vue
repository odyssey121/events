<template>
  <div>
    <div class="q-pa-md">
      <div class="row">
        <div class="col-md-12 col-sm-12">
          <q-table
            :grid="$q.screen.xs"
            title="Treats"
            :data="events"
            :columns="columns"
            row-key="name"
            :filter="filter"
          >
            <template v-slot:top-right>
              <q-input
                borderless
                dense
                debounce="300"
                v-model="filter"
                placeholder="Поиск по имени"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>
            <template v-slot:top-left>
              <div class="row" style>
                <q-input filled v-model="date" mask="date" :rules="['date']">
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        ref="qDateProxy"
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date v-model="date" @input="() => $refs.qDateProxy.hide()" />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <q-input filled v-model="date" mask="date" :rules="['date']">
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        ref="qDateProxy"
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date v-model="date" @input="() => $refs.qDateProxy.hide()" />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
            </template>
          </q-table>
        </div>
      </div>

      <div v-show="events" class="detail-splitter">
        <q-splitter v-model="splitterModel" style="height: 450px">
          <template v-slot:before>
            <div class="q-pa-md">
              <q-date v-model="date" :events="getEventsPoints" event-color="orange" />
            </div>
          </template>

          <template v-slot:after>
            <q-tab-panels
              v-model="date"
              animated
              transition-prev="jump-up"
              transition-next="jump-up"
            >
              <q-tab-panel
                v-for="(record, index) in events"
                :key="index"
                :name="$moment(record.event_date).format('YYYY/MM/DD')"
              >
                <div class="text-h4 q-mb-md">{{record.title}}</div>
                <p>{{record.description}}</p>
              </q-tab-panel>
            </q-tab-panels>
          </template>
        </q-splitter>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  middleware: "auth",
  components: {},
  computed: {
    getEventsPoints() {
      if (this.events) {
        return this.events.map(event =>
          this.$moment(event.event_date).format("YYYY/MM/DD")
        );
      }
      return [];
    }
  },
  data() {
    return {
      splitterModel: 50,
      date: this.$moment().format("YYYY/MM/DD"),
      filter: "",
      columns: [
        {
          name: "title",
          required: true,
          label: "имя",
          align: "left",
          field: row => row.title,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "description",
          align: "center",
          label: "описание",
          field: "description",
          sortable: true
        },
        {
          name: "event_date",
          label: "дата события",
          field: "event_date",
          format: val => this.$moment(val).format("h:mm:ss a, MMMM Do YYYY"),
          sortable: true
        }
      ]
    };
  },
  async asyncData({ $axios, error }) {
    let token,
      events,
      getEventsUrl = "/api/events/";
    token = localStorage.getItem("events_spa_token");
    $axios.setToken(`Token ${token}`);
    try {
      events = await $axios.$get(getEventsUrl);
    } catch (err) {
      console.log("GET_EVENTS_ERROR=>", err);
    }
    console.log(events);
    return { events };
  },
  methods: {
    onRowClick(evt, row) {
      console.log("clicked on", row);
    }
  }
};
</script>

<style>
.detail-splitter {
  margin-top: 12px;
}
</style>
