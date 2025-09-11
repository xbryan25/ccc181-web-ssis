import type { Row } from "@tanstack/vue-table";
import type { Student, Program, College } from "~/types";

export interface RowItem {
  type?: "label" | "separator";
  label?: string;
  onSelect?: () => void;
}

export function getRowItems<T extends Student | Program | College>(
  row: Row<T>,
  callbacks: {
    openEditDialog: () => void;
    openConfirmDeleteDialog: (row: T) => void;
  }
) {
  return [
    { type: "label", label: "Actions" },
    { type: "separator" },
    { label: "Edit", onSelect: callbacks.openEditDialog },
    { label: "Delete", onSelect: () => callbacks.openConfirmDeleteDialog(row.original) },
  ];
}