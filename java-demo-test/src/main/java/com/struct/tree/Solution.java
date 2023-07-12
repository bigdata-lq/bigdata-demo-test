package com.struct.tree;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

/**
 * @description:  二叉查找树 ：O(n) 节点有数字 左子树上所有结点的值均小于它的根结点的值
*                 平衡二叉搜索树 ：O(logn)  它是一棵空树或它的左右两个子树的高度差的绝对值不超过1，并且左右两个子树都是一棵平衡二叉树
 *                红黑树介于特殊的平衡二叉树,黑节点的数不得少于最长数 N -1 如最短子树黑色节点数为N 那最长的子树黑色节点数为2n-1
 *                应用： TreeSet & TreeMap & Linux虚拟内存
 * @author: liquan
 * @time: 2022/11/22 0022 上午 11:41
 */
public class Solution {

    /**
     * 前序遍历·递归·LC144_二叉树的前序遍历
     * @param root
     * @return
     */
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<Integer>();
        preorder(root, result);
        return result;
    }

    public void preorder(TreeNode root, List<Integer> result) {
        if (root == null) {
            return;
        }
        result.add(root.val);
        preorder(root.left, result);
        preorder(root.right, result);
    }

    /**
     * 中序遍历
     * @param root
     * @return
     */
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        inorder(root, res);
        return res;
    }

    void inorder(TreeNode root, List<Integer> list) {
        if (root == null) {
            return;
        }
        inorder(root.left, list);
        list.add(root.val);             // 注意这一句
        inorder(root.right, list);
    }

    public List<Integer> postorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        postorder(root, res);
        return res;
    }

    // 后序遍历·递归·LC145_二叉树的后序遍历
    void postorder(TreeNode root, List<Integer> list) {
        if (root == null) {
            return;
        }
        postorder(root.left, list);
        postorder(root.right, list);
        list.add(root.val);             // 注意这一句
    }

    // 层次遍历
    public static void levelOrder(TreeNode root){
        final LinkedList<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            root = queue.pop();
            System.out.println(root.val);
            if (root.left != null) queue.add(root.left);
            if (root.right != null) queue.add(root.right);
        }
    }

    //新增二叉树节点
    public TreeNode insertIntoBST(TreeNode root, int val) {
        if (root == null) return new TreeNode(val);
        TreeNode newRoot = root;
        TreeNode pre = root;
        while (root != null) {
            pre = root;
            if (root.val > val) {
                root = root.left;
            } else if (root.val < val) {
                root = root.right;
            }
        }
        if (pre.val > val) {
            pre.left = new TreeNode(val);
        } else {
            pre.right = new TreeNode(val);
        }

        return newRoot;
    }

    //新增二叉树节点 递归法
    public TreeNode insertIntoBST2(TreeNode root, int val) {
        if (root == null) // 如果当前节点为空，也就意味着val找到了合适的位置，此时创建节点直接返回。
            return new TreeNode(val);

        if (root.val < val){
            root.right = insertIntoBST(root.right, val); // 递归创建右子树
        }else if (root.val > val){
            root.left = insertIntoBST(root.left, val); // 递归创建左子树
        }
        return root;
    }

    /**
     * 删除树节点
     * @param root
     * @param key
     * @return
     */
    public TreeNode deleteNode(TreeNode root, int key) {
        root = delete(root,key);
        return root;
    }

    private TreeNode delete(TreeNode root, int key) {
        if (root == null) return null;

        if (root.val > key) {
            root.left = delete(root.left,key);
        } else if (root.val < key) {
            root.right = delete(root.right,key);
        } else {
            if (root.left == null) return root.right;
            if (root.right == null) return root.left;
            TreeNode tmp = root.right;
            while (tmp.left != null) {
                tmp = tmp.left;
            }
            root.val = tmp.val;
            root.right = delete(root.right,tmp.val);
        }
        return root;
    }



}
