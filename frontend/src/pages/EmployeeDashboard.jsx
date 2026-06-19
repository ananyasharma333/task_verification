import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const EmployeeDashboard = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-sm border border-slate-100 p-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-slate-800">Employee Dashboard</h1>
          <button 
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-medium text-slate-600 bg-slate-100 rounded-lg hover:bg-slate-200 transition-colors"
          >
            Logout
          </button>
        </div>
        <p className="text-slate-600">Welcome, <span className="font-medium text-slate-900">{user?.name}</span>!</p>
        <div className="mt-8 p-4 bg-blue-50 text-blue-800 rounded-lg border border-blue-100">
          You have Employee privileges. Here you can view and update your assigned tasks.
        </div>
      </div>
    </div>
  );
};

export default EmployeeDashboard;
