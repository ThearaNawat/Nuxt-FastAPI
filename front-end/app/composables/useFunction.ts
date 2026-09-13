import type { MenuNode } from "~~/store/state"

export const useFunction = () => {
    return {
        hasPermission: (path: string, permission: string) => hasButtonPermission(path, permission),
        hasRoutePermission: (menus: MenuNode[], path: string): boolean => hasRoutePermission(menus, path),
    }
}