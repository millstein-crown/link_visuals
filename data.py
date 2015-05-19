import MySQLdb
import json

def get_ciks(id_13f):
    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "adv_13f_match")
    cursor = db.cursor()

    cursor.execute("select company_name from thirteenf_groups where group_id = %i" % id_13f)
    ids = cursor.fetchall()
    ids = list(set([a[0].title() for a in ids]))

    db.close()

    return ids

def get_crds(id_adv):

    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "adv_new")
    cursor = db.cursor()

    cursor.execute("select name from adv_groups_final where group_id = %i" % id_adv)
    ids = cursor.fetchall()
    ids = list(set([a[0].title() for a in ids]))

    db.close()

    return ids

def get_group_ids(link_id):

    adv_ids = []
    cik_ids = []

    db = MySQLdb.connect("localhost", "root", "Edgar20!4", "adv_13f_match")
    cursor = db.cursor()

    cursor.execute("select adv_group_id, thirteenf_group_id from group_links_new_3 where link_id = %i" % link_id)
    ids = cursor.fetchall()
    for i in ids:
        adv_ids.append(i[0])
        cik_ids.append(i[1])

    db.close()
    return list(set(adv_ids)), list(set(cik_ids))

if __name__ == '__main__':

    link_list = []
    node_list = []
    group_count = 0
    index_count = 0

    for lk in [281, 2327]:

        group_count += 1

        node_list.append({"name": "LINK " + str(lk), "group": group_count})

        link_node_index = index_count
        group_ids = get_group_ids(lk)
        index_count += 1

        for g in group_ids[0]:
            node_list.append({"name": "ADV Group " + str(g), "group": group_count})
            link_list.append({"source": index_count, "target": link_node_index, "value": 1})
            group_count += 1
            source_count = index_count
            index_count += 1
            children = get_crds(g)
            for c in children:
                node_list.append({"name": str(c), "group": group_count})
                link_list.append({"source": index_count, "target": source_count, "value": 1})
                index_count += 1

        for g in group_ids[1]:
            group_count += 1
            node_list.append({"name": "13F Group " + str(g), "group": group_count})
            link_list.append({"source": index_count, "target": link_node_index, "value": 1})
            source_count = index_count
            index_count += 1
            children = get_ciks(g)
            for c in children:
                node_list.append({"name": str(c), "group": group_count})
                link_list.append({"source": index_count, "target": source_count, "value": 1})
                index_count += 1


    final_dict = {"nodes": node_list, "links": link_list}

    j = json.dumps(final_dict)
    json_file = 'grouplink.js'
    f = open(json_file, 'w')
    print >> f, j
