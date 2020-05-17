<template>
  <div>
    <div class="q-pa-md">
      <div class="row">
        <div class="col-md-12 col-sm-12">
          <q-table
            :grid="$q.screen.xs"
            title="Events"
            :data="events"
            :columns="columns"
            row-key="id"
            :filter="filter"
            @row-click="onRowClick"
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
              <div class="row">
                <q-input
                  style="width:134px;"
                  label="От"
                  filled
                  v-model="filter_range.from_date_range"
                  mask="date"
                  :rules="['date']"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        ref="qDateProxy1"
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date
                          v-model="filter_range.from_date_range"
                          @input="() => $refs.qDateProxy1.hide()"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <q-input
                  label="До"
                  filled
                  v-model="filter_range.to_date_range"
                  mask="date"
                  :rules="['date']"
                  style="width:134px;"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        ref="qDateProxy"
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date
                          v-model="filter_range.to_date_range"
                          @input="() => $refs.qDateProxy.hide()"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <q-btn
                  color="purple"
                  label="Приминить"
                  class="range-btn"
                  size="12px"
                  @click="submitFilterRange"
                />
                <q-btn
                  color="primary"
                  label="Сбросить"
                  class="range-btn"
                  size="12px"
                  @click="resetFilterRange"
                />
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
      filter_range: {
        from_date_range: this.$moment().format("YYYY-MM-DD HH:mm"),
        to_date_range: this.$moment().format("YYYY-MM-DD HH:mm")
      },
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
    return { events };
  },
  methods: {
    onRowClick(evt, { id }) {
      this.$router.history.push(`/event/${id}`);
    },
    submitFilterRange(e) {
      const { from_date_range, to_date_range } = this.filter_range;
      const rangeFilterUrl = `/api/events/?event_date=&start=${this.$moment(
        from_date_range
      ).toISOString()}&end=${this.$moment(to_date_range).toISOString()}`;
      console.log(rangeFilterUrl);
      const token = localStorage.getItem("events_spa_token");
      this.$axios.setToken(`Token ${token}`);
      this.$axios
        .$get(rangeFilterUrl)
        .then(data => {
          this.events = data;
        })
        .catch(err => console.log("FILTER RANGE ERR =>", err));
    },
    resetFilterRange(e) {
      let token,
        getEventsUrl = "/api/events/";
      token = localStorage.getItem("events_spa_token");
      this.$axios.setToken(`Token ${token}`);
      this.$axios
        .$get(getEventsUrl)
        .then(data => {
          this.events = data;
        })
        .catch(err => console.log("RESET FILTER RANGE ERR =>", err));
    }
  }
};
</script>

<style>
.detail-splitter {
  margin-top: 12px;
}
#main-layout
  > div.container
  .q-table__top.relative-position.row.items-center
  > div.q-table-control
  > div
  > label:nth-child(1) {
  margin-right: 12px;
}
.range-btn {
  width: 84px;
  margin-left: 12px;
  height: 56px;
}
</style>
