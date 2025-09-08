<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
  entityType: string;
  dialogType: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const visible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit("update:modelValue", value),
});

const entityPropertiesOptions = {
  students: [
    "ID Number",
    "First Name",
    "Last Name",
    "Year Level",
    "Gender",
    "Program Code",
  ],
  programs: ["Program Code", "Program Name", "College Code"],
  colleges: ["College Name", "College Code"],
};

const filterTypes = ["Starts With", "Ends With", "Contains"];

const sortTypes = ["Ascending", "Descending"];
</script>

<template>
  <div>
    <Dialog v-model:visible="visible" modal class="w-[30rem]">
      <template #header>
        <h2 v-if="props.dialogType === 'filter'" class="text-3xl font-semibold">
          Search Filters
        </h2>

        <h2 v-else class="text-3xl font-semibold">Sort Options</h2>
      </template>
      <div>
        <div class="flex-col mb-12">
          <div
            v-if="props.dialogType === 'filter'"
            class="w-full flex gap-4 mb-2"
          >
            <h3 class="flex-1 text-lg font-medium">Search By</h3>
            <h3 class="flex-1 text-lg font-medium">Search Type</h3>
          </div>
          <div v-else class="w-full flex gap-4 mb-2">
            <h3 class="flex-1 text-lg font-medium">Sort Field</h3>
            <h3 class="flex-1 text-lg font-medium">Sort Order</h3>
          </div>
          <div class="w-full flex gap-4 mb-2">
            <div class="flex-1 h-[2px] bg-white" />
            <div class="flex-1 h-[2px] bg-white" />
          </div>
          <div class="w-full flex gap-4 mb-4">
            <RadioSelectButtons
              :options="entityPropertiesOptions[props.entityType]"
            />
            <RadioSelectButtons
              v-if="props.dialogType === 'filter'"
              :options="filterTypes"
            />
            <RadioSelectButtons v-else :options="sortTypes" />
          </div>
        </div>
      </div>

      <div class="flex justify-end gap-2">
        <Button
          type="button"
          label="Cancel"
          severity="secondary"
          @click="visible = false"
        />
        <Button type="submit" label="Proceed" @click="visible = false" />
      </div>
    </Dialog>
  </div>
</template>
