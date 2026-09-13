import type { MenuNode } from '~~/store/state'
import { useAuthStore } from '~~/store/state'
export const hasButtonPermission = (label: string, permission: string) => {
    const authStore = useAuthStore()
    const menuData = authStore.getMenuAll
    const menuIds = authStore.getUser?.role?.menu
    const menu = getFlattenMenus(menuData).find((menu: MenuNode) => menu.label.toLocaleLowerCase().trim() === label)
    return (
        menu?.children?.some((child: MenuNode) => child.type === 'BUTTON' && child.label.toLocaleLowerCase().trim() === permission.toLocaleLowerCase().trim() && menuIds?.includes(child.id!)) ?? false
    )
}

export const hasRoutePermission = (
    menus: MenuNode[],
    path: string
): boolean => {
    return getFlattenMenus(menus).some(
        menu =>
            menu.type === "MENU" &&
            menu.path === path
    );
}

const getFlattenMenus = (menus: MenuNode[]): MenuNode[] => {
    return menus.flatMap((menu: MenuNode) => [menu, ...(menu.children ? getFlattenMenus(menu.children) : [])])
}

