<script setup lang="ts">
const props = defineProps<{
  options: string[];
  dialogType: string;
  columnPosition: string;
  searchAndSortState: {
    searchBy: string;
    searchType: string;
    sortField: string;
    sortOrder: string;
  };
}>();

const emit = defineEmits<{
  (
    e:
      | "update:searchBy"
      | "update:searchType"
      | "update:sortField"
      | "update:sortOrder",
    value: string
  ): void;
}>();

const selectedOption = computed({
  get: () => determineValueToGet(),
  set: (value: string) => determineEmitToReturn(value),
});

const determineValueToGet = () => {
  if (props.dialogType === "filter") {
    if (props.columnPosition === "first") {
      return props.searchAndSortState.searchBy;
    } else {
      return props.searchAndSortState.searchType;
    }
  } else {
    if (props.columnPosition === "first") {
      return props.searchAndSortState.sortField;
    } else {
      return props.searchAndSortState.sortOrder;
    }
  }
};

const determineEmitToReturn = (value: string) => {
  if (props.dialogType === "filter") {
    if (props.columnPosition === "first") {
      emit("update:searchBy", value);
    } else {
      emit("update:searchType", value);
    }
  } else {
    if (props.columnPosition === "first") {
      emit("update:sortField", value);
    } else {
      emit("update:sortOrder", value);
    }
  }
};

const handleClick = (option: string) => {
  selectedOption.value = option;
  console.log(props.searchAndSortState);
};
</script>

<template>
  <div class="flex-1 flex flex-col gap-2">
    <button
      v-for="(option, index) in options"
      :key="index"
      :class="[
        'w-full h-10 rounded-lg transition-colors duration-100',
        selectedOption === option
          ? 'bg-zinc-700 text-white'
          : 'text-white hover:bg-zinc-700',
      ]"
      @click="handleClick(option)"
    >
      <p class="font-medium">{{ option }}</p>
    </button>
  </div>
</template>
